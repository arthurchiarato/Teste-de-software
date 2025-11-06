# SGBU - Sistema de Gestão de Biblioteca Universitária
## Módulo de Empréstimo e Devolução

## Overview
This is a Flask-based library loan management system (SGBU - Equipe 3) that manages book loans and returns for a university library. The application includes both a web interface and REST API endpoints.

**Current State:** Fully configured and running on Replit with proper development and deployment settings.

## Recent Changes (2024-11-06)
- Installed Python 3.11 and all required dependencies (Flask, SQLAlchemy, etc.)
- Created `run.py` script to run Flask on 0.0.0.0:5000 for Replit environment
- Created `wsgi.py` for production deployment with gunicorn
- Configured workflow to run Flask app on port 5000 with webview
- Set up deployment configuration using autoscale with gunicorn
- Created .gitignore for Python/Flask projects
- Application successfully tested and verified working

## Project Architecture

### Technology Stack
- **Backend:** Flask 3.0.3 with Flask-SQLAlchemy 3.1.1
- **Database:** SQLite (sgbu.db) - development database with sample data
- **Frontend:** HTML templates with Bootstrap 5.3.3 (Jinja2)
- **Testing:** pytest with pytest-flask
- **Production Server:** gunicorn

### Directory Structure
```
sgbu_equipe3_emprestimos/
├── app/
│   ├── app.py          # Flask application and routes
│   ├── models.py       # SQLAlchemy models (User, Book, Loan)
│   ├── seed.py         # Sample data loader
│   └── templates/      # Jinja2 HTML templates
│       ├── base.html
│       ├── index.html
│       └── loans.html
├── tests/
│   ├── conftest.py
│   ├── test_unit_loans.py
│   └── test_contracts.py
└── requirements.txt
```

### Database Models
1. **User** - Library users (students, professors, staff)
   - Fields: id, name, matricula (unique), user_type
   
2. **Book** - Book catalog
   - Fields: id, title, author, available (boolean)
   
3. **Loan** - Loan records
   - Fields: id, user_id, book_id, loan_date, due_date, return_date
   - Relationships: user, book

### Key Features
- Create new book loans with customizable loan period (default: 7 days)
- Track loan status (open/returned)
- Automatic book availability management
- Return processing with validation
- List and filter loans (all/open only)
- RESTful API endpoints for integrations

## API Endpoints

### REST API
- `POST /api/loans` - Create new loan
  - Body: `{user_id, book_id, loan_days}`
- `GET /api/loans` - List loans
  - Query: `status=abertos|todos`
- `GET /api/loans/<loan_id>` - Get loan details
- `POST /api/loans/<loan_id>/return` - Register book return

### Frontend Routes
- `GET /` - Homepage
- `GET /loans` - Loans management page
- `POST /loans/new` - Create new loan (form)
- `POST /loans/<loan_id>/return` - Return book (form)

## Business Rules
- Books can only be loaned if `available == True`
- Default loan period is 7 days (configurable)
- On return, book automatically becomes available again
- Cannot return an already returned loan

## Running the Application

### Development
The Flask app is configured to run automatically on Replit:
- Runs on: `0.0.0.0:5000`
- Debug mode: enabled
- Auto-reload: enabled

### Testing
```bash
pytest -q
```

### Sample Data
The application automatically seeds sample data on first run:
- 2 sample users (Alice Silva - student, Prof. Bruno - professor)
- 3 sample books (Clean Code, Introdução a Algoritmos, Arquitetura de Software)

## Deployment
The application is configured for Replit's autoscale deployment:
- Uses gunicorn WSGI server
- Binds to port 5000
- Stateless design suitable for autoscaling

## Notes
- This module was designed to work standalone but can integrate with other SGBU modules (User Management, Catalog)
- For production, consider connecting to external user and book management services
- Database is SQLite for development; consider PostgreSQL for production
- Sample data is loaded automatically for testing and evaluation purposes
