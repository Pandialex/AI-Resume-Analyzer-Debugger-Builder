ARDAA AI - AI Resume Analyzer, Debugger & Builder
https://img.shields.io/badge/ARDAA-AI-blue
https://img.shields.io/badge/Django-5.2.6-green
https://img.shields.io/badge/Python-3.13-blue
https://img.shields.io/badge/PostgreSQL-Database-blue

🚀 Overview
ARDAA AI is an intelligent resume analysis platform that leverages AI to help job seekers optimize their resumes, identify areas for improvement, and build professional CVs. Get instant feedback on your resume's strengths and weaknesses with our advanced AI-powered analysis.

🌐 Live Demo
Visit: ai-resume-analyzer-debugger-builder.onrender.com

✨ Features
🔍 Resume Analysis
AI-Powered Analysis: Get detailed feedback on your resume content

ATS Optimization: Ensure your resume passes through Applicant Tracking Systems

Skill Gap Analysis: Identify missing skills for your target roles

Formatting Check: Professional formatting recommendations

🛠️ Resume Building
Professional Templates: Choose from multiple modern resume templates

Content Suggestions: AI-generated content for different job roles

Real-time Preview: See changes instantly as you build

Export Options: Download in PDF, Word, and other formats

💬 AI Chat Assistant
Career Guidance: Get personalized career advice

Interview Preparation: Practice with AI-powered mock interviews

Cover Letter Help: Generate compelling cover letters

Career Path Suggestions: Explore suitable career paths

👤 User Management
Quick Registration: Simple email-based signup (No OTP required)

Profile Management: Complete user profiles with career information

Usage Tracking: Monitor your resume analysis usage

Secure Authentication: Django-powered secure login system

🛠️ Technology Stack
Backend
Framework: Django 5.2.6

Database: PostgreSQL

Authentication: Django Auth with custom User model

API: Django REST Framework (if applicable)

Frontend
Templating: Django Templates

Styling: Custom CSS with modern glassmorphism design

Icons: Font Awesome 6.4.0

Fonts: Google Fonts (Inter)

AI & External Services
AI Engine: Google Gemini API

Email Service: SendGrid (Optional, for welcome emails)

File Processing: PDF and DOCX parsing

Hosting: Render.com

Security
CSRF Protection: Enabled with secure cookies

Session Management: Secure session handling

Password Validation: Django's built-in validators

HTTPS: Enforced in production

📦 Installation & Setup
Prerequisites
Python 3.8+

PostgreSQL 12+

Git

Local Development
Clone the Repository

bash
git clone https://github.com/your-username/ardaa-ai.git
cd ardaa-ai
Create Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
pip install -r requirements.txt
Environment Configuration
Create a .env file in the root directory:

env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://username:password@localhost:5432/ardaa_db
GEMINI_API_KEY=your-gemini-api-key
SENDGRID_API_KEY=your-sendgrid-key  # Optional
Database Setup

bash
python manage.py migrate
python manage.py createsuperuser
Run Development Server

bash
python manage.py runserver
Visit: http://localhost:8000

Production Deployment
Environment Variables on Render

env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=your-render-postgres-url
GEMINI_API_KEY=your-gemini-api-key
SENDGRID_API_KEY=your-sendgrid-key  # Optional
Build Commands

bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
🏗️ Project Structure
text
AI_Analyzer/
├── accounts/                 # User authentication & profiles
│   ├── views.py             # Authentication views
│   ├── models.py            # Custom User model
│   ├── urls.py              # Auth routes
│   └── templates/           # Auth templates
├── ARDAA/                   # Main application
│   ├── views.py             # Core views
│   ├── urls.py              # Main routes
│   └── templates/           # Main templates
├── resumebuild/             # Resume building functionality
│   ├── views.py             # Resume builder views
│   └── templates/           # Resume templates
├── chat/                    # AI chat functionality
│   ├── views.py             # Chat views
│   └── templates/           # Chat interfaces
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── images/              # Images & icons
└── media/                   # User uploaded files
🔧 Configuration
Database
The project uses PostgreSQL with the following configuration:

Local: Direct PostgreSQL connection

Production: Render PostgreSQL with connection pooling

Email Setup (Optional)
Welcome emails are optional. Configure SendGrid for production:

python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
File Uploads
Maximum file size: 10MB

Supported formats: PDF, DOC, DOCX, TXT

Secure file handling with Django's media system

🎯 Usage Guide
For Job Seekers
Register: Quick signup with email and password

Upload Resume: Submit your current resume for analysis

Get Insights: Receive detailed AI-powered feedback

Build Resume: Use our builder to create professional resumes

Chat with AI: Get career advice and interview tips

Resume Analysis Includes
✅ Content quality assessment

✅ ATS compatibility score

✅ Keyword optimization

✅ Formatting recommendations

✅ Skill gap analysis

✅ Industry-specific suggestions

🔒 Security Features
Secure password hashing with Django Auth

CSRF protection on all forms

XSS protection headers

Secure session management

File upload validation

Production security settings

📊 API Documentation
Available Endpoints
POST /accounts/register/ - User registration

POST /accounts/login/ - User authentication

POST /accounts/logout/ - User logout

GET /accounts/profile/ - User profile

POST /resume/analyze/ - Resume analysis

GET /chat/ - AI chat interface

🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Development Guidelines
Follow PEP 8 coding standards

Write meaningful commit messages

Add tests for new features

Update documentation accordingly

🐛 Troubleshooting
Common Issues
Database Connection Error

Check PostgreSQL is running

Verify DATABASE_URL in environment variables

Static Files Not Loading

Run python manage.py collectstatic

Check WhiteNoise configuration

Gemini API Errors

Verify GEMINI_API_KEY is set

Check API quota and limits

Email Issues

Welcome emails are optional

Check SendGrid configuration if enabled

Debug Mode
Set DEBUG=True in development for detailed error messages.

📄 License
This project is licensed under the MIT License - see the LICENSE.md file for details.

🙏 Acknowledgments
Google Gemini AI for powering our analysis engine

Django community for the excellent web framework

Render.com for reliable hosting

All our contributors and testers

📞 Support
For support and questions:

📧 Email: support@ardaa.ai

🐛 Issues: GitHub Issues

📚 Documentation: Project Wiki

🚀 Deployment Status
https://img.shields.io/badge/Render-Deployed-success

ARDAA AI - Empowering your career journey with AI-powered resume optimization and career guidance. 
created by Alex Pandian M -Madurai Tamilnadu India

Built with ❤️ using Django and modern web technologies.

