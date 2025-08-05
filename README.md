# HESC Smart Aid Assistant

A comprehensive web application designed to streamline financial aid eligibility screening and management for the Higher Education Services Corporation (HESC).

## About This Project

The HESC Smart Aid Assistant provides a dual-portal system serving both students and financial aid administrators:

### 🎓 Student Portal
- **Eligibility Screener**: Interactive form to check qualification for multiple financial aid programs
- **Document Management**: Track required documents and submission status
- **Instant Reports**: Generate comprehensive eligibility summaries
- **AI Chatbot**: Get instant answers to common financial aid questions
- **User Authentication**: Secure login system for personalized experience

### 👨‍💼 Employee Portal
- **Student Management**: View and search student records
- **Eligibility Verification**: Review and approve student applications
- **Document Tracking**: Monitor document submission status
- **Report Generation**: Create detailed student financial aid reports
- **Administrative Tools**: Comprehensive management interface

## Features

- **Multi-Program Support**: TAP, Pell Grant, Excelsior Scholarship, SEOG, and Enhanced Tuition Award
- **Real-time Eligibility Assessment**: Instant feedback on program qualification
- **Document Workflow**: Complete tracking from submission to verification
- **Responsive Design**: Optimized for desktop and mobile devices
- **Dual Authentication**: Separate login systems for students and employees
- **Data Persistence**: Session-based data storage with JSON file backup

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
- **Styling**: Custom CSS with responsive design
- **Deployment**: Railway
- **Authentication**: Session-based management

## Getting Started

### Local Development

1. **Navigate to the project directory**:
   ```bash
   cd /Users/gracieevans/code/hesc_screener
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to: http://127.0.0.1:5000

### Employee Test Accounts

For testing the employee portal, use these credentials:

- **Admin**: `admin` / `hesc2024`
- **Staff Member**: `staff1` / `staff123`
- **Senior Advisor**: `staff2` / `advisor456`

## How to Use

1. **Start with the Eligibility Screener**: Click "Start Screening" on the home page
2. **Fill out the form** with your residency, GPA, income, and enrollment status
3. **View your results** in the comprehensive eligibility report
4. **Track documents** for programs you're eligible for
5. **Use the chatbot** (💬 icon in bottom-right) for questions

## Project Structure

```
hesc_screener/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── railway.json          # Railway service configuration
├── data/
│   ├── aid_programs.csv  # Financial aid program data
│   ├── faq.json         # Chatbot knowledge base
│   └── students.json    # Student records database
├── templates/           # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Homepage
│   ├── screener.html   # Eligibility screening form
│   ├── documents.html  # Document management
│   ├── report.html     # Student reports
│   └── employee_*.html # Employee portal pages
└── static/             # Static assets (if any)
```

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

## Data Sources

- **Aid Programs**: Comprehensive database of NY state and federal financial aid programs
- **FAQ Database**: Curated responses for common financial aid questions
- **Student Records**: Demo data for testing employee portal functionality

## Security Features

- Environment-based configuration for production
- Session management for user authentication
- Input validation and sanitization
- Secure credential handling

## Deployment

This application is configured for deployment on Railway with:
- Automatic build detection
- Environment variable support
- Health check monitoring
- Restart policies for reliability

## For Developers

To modify program data, edit `data/aid_programs.csv`. To add FAQ responses, update `data/faq.json`.

The application uses Flask sessions to maintain user data throughout the screening process.

## Contributing

This project was developed as a comprehensive financial aid management system. For questions or contributions, please refer to the project documentation.

---

**Built with ❤️ for educational financial aid management**

*This is a demonstration project showcasing modern web development practices for educational administration systems.*