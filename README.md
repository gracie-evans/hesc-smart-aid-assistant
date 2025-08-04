# HESC Smart Aid Assistant

A comprehensive web application for financial aid eligibility screening, document tracking, and student assistance.

## Features

- **Eligibility Screener**: Interactive form to check eligibility for multiple financial aid programs
- **Document Verification**: Track and simulate document uploads for eligible programs
- **Instant Reports**: Comprehensive eligibility reports with award amounts and deadlines
- **AI Chatbot**: Floating chat assistant with FAQ support for common financial aid questions
- **Professional UI**: Modern, responsive design optimized for students and administrators

## Quick Start

1. **Navigate to the project directory**:
   ```bash
   cd /Users/gracieevans/code/hesc_screener
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to: http://127.0.0.1:5000

## How to Use

1. **Start with the Eligibility Screener**: Click "Start Screening" on the home page
2. **Fill out the form** with your residency, GPA, income, and enrollment status
3. **View your results** in the comprehensive eligibility report
4. **Track documents** for programs you're eligible for
5. **Use the chatbot** (💬 icon in bottom-right) for questions

## Application Structure

- `app.py` - Main Flask application with all routes and logic
- `data/aid_programs.csv` - Financial aid program data with eligibility rules
- `data/faq.json` - FAQ data for the chatbot
- `templates/` - HTML templates with modern styling
- `requirements.txt` - Python dependencies

## Available Programs

The application includes 8 financial aid programs:
- TAP (Tuition Assistance Program)
- Pell Grant
- Excelsior Scholarship
- SEOG (Supplemental Educational Opportunity Grant)
- NYS Dream Act
- Enhanced Tuition Award
- Part-Time TAP
- College Choice Tuition Program

## Demo Features

- **Document Upload**: Simulated for demonstration (no actual file storage)
- **Eligibility Logic**: Real calculations based on program requirements
- **Session Management**: Data persists during your browser session
- **Responsive Design**: Works on desktop and mobile devices

## For Developers

To modify program data, edit `data/aid_programs.csv`. To add FAQ responses, update `data/faq.json`.

The application uses Flask sessions to maintain user data throughout the screening process.

---

**Built for HESC Government RFP Demonstration**