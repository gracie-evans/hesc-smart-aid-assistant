from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import pandas as pd
import json
import os
from datetime import datetime
import difflib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'hesc_smart_aid_2024'  # For session management

# Load program eligibility rules
csv_path = os.path.join("data", "aid_programs.csv")
programs_df = pd.read_csv(csv_path)

# Load FAQ data
faq_path = os.path.join("data", "faq.json")
with open(faq_path, "r") as f:
    faq_data = json.load(f)

# Hardcoded employee accounts
EMPLOYEE_ACCOUNTS = {
    'admin': {'password': 'hesc2024', 'name': 'Administrator', 'role': 'Admin'},
    'staff1': {'password': 'staff123', 'name': 'Jane Smith', 'role': 'Financial Aid Counselor'},
    'staff2': {'password': 'advisor456', 'name': 'Michael Johnson', 'role': 'Senior Advisor'}
}

# Employee authentication decorator
def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'employee_logged_in' not in session:
            flash('Please log in to access the employee dashboard.', 'error')
            return redirect(url_for('employee_login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper functions for student data
def load_students():
    students_path = os.path.join("data", "students.json")
    try:
        with open(students_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(students_data):
    students_path = os.path.join("data", "students.json")
    with open(students_path, "w") as f:
        json.dump(students_data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/screener")
def screener():
    return render_template("screener.html")

@app.route("/documents")
def documents():
    if 'eligibility_results' not in session:
        return redirect(url_for('screener'))
    return render_template("documents.html")

@app.route("/report")
def report():
    if 'eligibility_results' not in session:
        return redirect(url_for('screener'))
    return render_template("report.html")

@app.route("/check_eligibility", methods=["POST"])
def check_eligibility():
    residency = request.form.get("residency")
    gpa = float(request.form.get("gpa", 0))
    income = float(request.form.get("income", 0))
    enrollment = request.form.get("enrollment")

    results = []
    eligible_programs = []
    ineligible_programs = []

    for _, row in programs_df.iterrows():
        eligible = True
        reasons = []
        
        # Check residency
        if row["residency_required"] != "Any" and row["residency_required"] != residency:
            eligible = False
            reasons.append(f"Residency requirement not met (requires {row['residency_required']})")
        
        # Check GPA
        if gpa < row["min_gpa"]:
            eligible = False
            reasons.append(f"GPA requirement not met (requires {row['min_gpa']})")
        
        # Check income
        if income > row["max_income"]:
            eligible = False
            reasons.append(f"Income too high (maximum ${row['max_income']:,})")
        
        # Check enrollment
        enrollment_required = row["enrollment_required"] == "Yes"
        enrollment_status = enrollment == "Yes"
        if enrollment_required and not enrollment_status:
            eligible = False
            reasons.append("Must be enrolled full-time")

        program_info = {
            "program": row["program_name"],
            "eligible": eligible,
            "reasons": reasons,
            "award_amount": row["award_amount"],
            "deadline": row["deadline"],
            "description": row["description"],
            "required_documents": row["required_documents"].split(";")
        }

        results.append(program_info)
        
        if eligible:
            eligible_programs.append(program_info)
        else:
            ineligible_programs.append(program_info)

    # Store results in session
    session['eligibility_results'] = results
    session['user_data'] = {
        'residency': residency,
        'gpa': gpa,
        'income': income,
        'enrollment': enrollment
    }
    session['eligible_programs'] = eligible_programs
    session['ineligible_programs'] = ineligible_programs
    
    # Initialize document tracking
    if 'documents' not in session:
        session['documents'] = {}
    
    for program in eligible_programs:
        program_name = program['program']
        if program_name not in session['documents']:
            session['documents'][program_name] = {}
            for doc in program['required_documents']:
                session['documents'][program_name][doc] = {'status': 'Pending', 'uploaded_date': None}

    return redirect(url_for('report'))

@app.route("/upload_document", methods=["POST"])
def upload_document():
    program = request.form.get("program")
    document = request.form.get("document")
    
    if 'documents' not in session:
        session['documents'] = {}
    
    if program not in session['documents']:
        session['documents'][program] = {}
    
    session['documents'][program][document] = {
        'status': 'Received',
        'uploaded_date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    session.modified = True
    return jsonify({"status": "success", "message": f"Document {document} uploaded for {program}"})

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_question = request.json.get("question", "").lower().strip()
    
    # Find best matching FAQ entry
    best_match = None
    best_score = 0
    
    for key, answer in faq_data.items():
        # Check if user question contains key words
        if key.lower() in user_question:
            best_match = answer
            break
        
        # Use difflib for fuzzy matching
        score = difflib.SequenceMatcher(None, user_question, key.lower()).ratio()
        if score > best_score and score > 0.3:  # Minimum threshold
            best_score = score
            best_match = answer
    
    if best_match:
        response = best_match
    else:
        response = "I'm sorry, I don't have information about that specific question. Please try asking about TAP, Pell Grant, Excelsior Scholarship, eligibility requirements, documents needed, deadlines, or application processes."
    
    return jsonify({"response": response})

@app.route("/api/user_data")
def get_user_data():
    return jsonify({
        'eligibility_results': session.get('eligibility_results', []),
        'eligible_programs': session.get('eligible_programs', []),
        'ineligible_programs': session.get('ineligible_programs', []),
        'documents': session.get('documents', {}),
        'user_data': session.get('user_data', {})
    })

@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect(url_for('home'))

# Employee Routes
@app.route("/employee-login")
def employee_login():
    return render_template("employee_login.html")

@app.route("/employee-login", methods=["POST"])
def employee_login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username in EMPLOYEE_ACCOUNTS and EMPLOYEE_ACCOUNTS[username]['password'] == password:
        session['employee_logged_in'] = True
        session['employee_username'] = username
        session['employee_name'] = EMPLOYEE_ACCOUNTS[username]['name']
        session['employee_role'] = EMPLOYEE_ACCOUNTS[username]['role']
        flash(f'Welcome, {EMPLOYEE_ACCOUNTS[username]["name"]}!', 'success')
        return redirect(url_for('employee_dashboard'))
    else:
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('employee_login'))

@app.route("/employee-logout")
def employee_logout():
    session.pop('employee_logged_in', None)
    session.pop('employee_username', None)
    session.pop('employee_name', None)
    session.pop('employee_role', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route("/employee-dashboard")
@employee_required
def employee_dashboard():
    search_query = request.args.get('search', '')
    students = load_students()
    
    if search_query:
        # Filter students based on search query
        filtered_students = []
        for student in students:
            if (search_query.lower() in student['name'].lower() or 
                search_query.lower() in student['student_id'].lower() or
                search_query.lower() in student.get('email', '').lower()):
                filtered_students.append(student)
        students = filtered_students
    
    return render_template("employee_dashboard.html", students=students, search_query=search_query)

@app.route("/employee/student/<student_id>")
@employee_required
def view_student(student_id):
    students = load_students()
    student = next((s for s in students if s['student_id'] == student_id), None)
    
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('employee_dashboard'))
    
    return render_template("student_detail.html", student=student)

@app.route("/employee/student/<student_id>/update", methods=["POST"])
@employee_required
def update_student(student_id):
    students = load_students()
    student_index = next((i for i, s in enumerate(students) if s['student_id'] == student_id), None)
    
    if student_index is None:
        return jsonify({"status": "error", "message": "Student not found"})
    
    data = request.json
    action = data.get('action')
    
    if action == 'update_verification':
        program_name = data.get('program')
        verified = data.get('verified')
        
        for program in students[student_index]['eligibility_results']:
            if program['program'] == program_name:
                program['verified'] = verified
                break
    
    elif action == 'add_document':
        program_name = data.get('program')
        document = data.get('document')
        
        for program in students[student_index]['eligibility_results']:
            if program['program'] == program_name:
                if document not in program['submitted_documents']:
                    program['submitted_documents'].append(document)
                if document in program['missing_documents']:
                    program['missing_documents'].remove(document)
                break
    
    elif action == 'remove_document':
        program_name = data.get('program')
        document = data.get('document')
        
        for program in students[student_index]['eligibility_results']:
            if program['program'] == program_name:
                if document in program['submitted_documents']:
                    program['submitted_documents'].remove(document)
                if document not in program['missing_documents']:
                    program['missing_documents'].append(document)
                break
    
    elif action == 'update_notes':
        notes = data.get('notes')
        students[student_index]['notes'] = notes
    
    elif action == 'add_missing_document':
        program_name = data.get('program')
        document = data.get('document')
        
        for program in students[student_index]['eligibility_results']:
            if program['program'] == program_name:
                if document not in program['missing_documents']:
                    program['missing_documents'].append(document)
                break
    
    elif action == 'remove_missing_document':
        program_name = data.get('program')
        document = data.get('document')
        
        for program in students[student_index]['eligibility_results']:
            if program['program'] == program_name:
                if document in program['missing_documents']:
                    program['missing_documents'].remove(document)
                break
    
    # Update last_updated timestamp
    students[student_index]['last_updated'] = datetime.now().isoformat()
    
    # Save updated data
    save_students(students)
    
    return jsonify({"status": "success", "message": "Student record updated successfully"})

@app.route("/employee/student/<student_id>/report")
@employee_required
def generate_student_report(student_id):
    students = load_students()
    student = next((s for s in students if s['student_id'] == student_id), None)
    
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('employee_dashboard'))
    
    # Calculate totals
    total_eligible_amount = sum(program['award_amount'] for program in student['eligibility_results'] if program['eligible'])
    eligible_programs = [p for p in student['eligibility_results'] if p['eligible']]
    ineligible_programs = [p for p in student['eligibility_results'] if not p['eligible']]
    
    return render_template("student_report.html", 
                         student=student, 
                         total_eligible_amount=total_eligible_amount,
                         eligible_programs=eligible_programs,
                         ineligible_programs=ineligible_programs)

@app.route("/employee/students/search")
@employee_required
def search_students():
    query = request.args.get('q', '').lower()
    students = load_students()
    
    if not query:
        return jsonify([])
    
    results = []
    for student in students:
        if (query in student['name'].lower() or 
            query in student['student_id'].lower() or 
            query in student.get('email', '').lower()):
            results.append({
                'student_id': student['student_id'],
                'name': student['name'],
                'email': student.get('email', ''),
                'status': student.get('status', 'Active')
            })
    
    return jsonify(results[:10])  # Limit to 10 results

if __name__ == "__main__":
    print("🚀 Starting HESC Smart Aid Assistant...")
    print("📍 Application will be available at:")
    print("   • http://127.0.0.1:5000")
    print("   • http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)