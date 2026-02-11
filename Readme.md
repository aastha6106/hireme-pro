# HireMe Pro

A production-ready resume builder built with Flask. Users can create accounts, build structured resumes with a live preview editor, and export clean PDFs. Designed as a SaaS foundation — authentication, authorization, CRUD, and PDF generation are all implemented and ready to extend.

Built with vanilla technologies. No frontend frameworks, no CSS libraries, no unnecessary dependencies.

---

## Live Features

- **User authentication** — Register, login, logout with secure password hashing
- **Resume CRUD** — Create, edit, and delete resumes with ownership protection
- **Structured sections** — Experience, education, and skills as separate managed entries
- **Live preview editor** — Split-screen builder with real-time preview updates
- **PDF export** — One-click download with professional formatting
- **Dark mode** — Toggle with localStorage persistence and OS preference detection
- **Responsive design** — Works on desktop, tablet, and mobile
- **Route protection** — Users can only access and modify their own data

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask, Python 3 |
| Auth | Flask-Login, Werkzeug security |
| Database | SQLAlchemy ORM, SQLite (dev), PostgreSQL ready |
| PDF | pdfkit + wkhtmltopdf |
| Frontend | Vanilla JS, custom CSS |
| Server | Gunicorn compatible |

## Project Structure

```
hireme-pro/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/main.css
│   │   └── js/preview.js
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── resume_edit.html
│       ├── resume_detail.html
│       ├── resume_form.html
│       ├── resume_pdf.html
│       ├── education_form.html
│       ├── experience_form.html
│       └── skill_form.html
├── config.py
├── run.py
└── requirements.txt
```

## Local Setup

```bash
git clone https://github.com/yourusername/hireme-pro.git
cd hireme-pro
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Visit `http://127.0.0.1:5000`

**Note:** PDF export requires wkhtmltopdf installed on your system.
See [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html) for installation.

## Database

SQLite for local development. Switch to PostgreSQL for production with one environment variable:

```bash
export DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Session signing | Dev key (change in production) |
| `DATABASE_URL` | Database connection | SQLite local file |
| `WKHTMLTOPDF_PATH` | PDF binary location | System default |

## Security

- Passwords hashed with Werkzeug
- Session-based auth via Flask-Login
- Ownership verification on every resume route
- POST-only destructive actions
- All queries through SQLAlchemy ORM

## Screenshots

See below for application walkthrough.

### Landing Page
![Landing Page](screenshots/01-landing-hero.png)

### Dashboard
![Dashboard](screenshots/07-dashboard-with-resumes.png)

### Resume Builder
![Builder](screenshots/08-builder-split-view.png)

### PDF Export
![PDF](screenshots/11-pdf-output.png)

### Dark Mode
![Dark Mode](screenshots/12-dark-mode-landing.png)

## License

MIT