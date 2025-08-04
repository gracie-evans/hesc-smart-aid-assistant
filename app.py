from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import json
import os
from datetime import datetime
import difflib

app = Flask(__name__)
app.secret_key = 'hesc_smart_aid_2024'  # For session management

# Load program eligibility rules
csv_path = os.path.join("data", "aid_programs.csv")
programs_df = pd.read_csv(csv_path)

# Load FAQ data
faq_path = os.path.join("data", "faq.json")
with open(faq_path, "r") as f:
    faq_data = json.load(f)

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

if __name__ == "__main__":
    print("🚀 Starting HESC Smart Aid Assistant...")
    print("📍 Application will be available at:")
    print("   • http://127.0.0.1:5000")
    print("   • http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)