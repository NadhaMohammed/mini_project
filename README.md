# EventHub

A multi-tenant event management platform for colleges. Admins can create and manage events, track student registrations via Google Sheets integration, and automatically notify subscribers via email.

## Features

- **Multi-Tenant Architecture** — Each college gets its own admin account with a unique college code
- **Event Management** — Create, update, and delete events with image uploads
- **Email Notifications** — Subscribers receive automatic emails when events are created or updated
- **Google Sheets Sync** — Import student registrations directly from Google Forms response sheets
- **Attendance Tracking** — Mark and manage student attendance per event
- **Reports Dashboard** — View event statistics and attendance reports
- **Public Event Directory** — Browse events across all colleges on the landing page

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| Database | Supabase (PostgreSQL) |
| Email | Gmail SMTP via Flask-Mail |
| Sheets | Google Sheets API (gspread) |
| Frontend | HTML, CSS, JavaScript |

## Setup

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd eventhub-demo
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Supabase anon/publishable key |
| `SECRET_KEY` | Flask session secret (any random string) |
| `MAIL_USERNAME` | Gmail address for sending notifications |
| `MAIL_PASSWORD` | Gmail App Password ([how to create](https://myaccount.google.com/apppasswords)) |

### 3. Set Up Database

Run `schema.sql` in your [Supabase SQL Editor](https://supabase.com/dashboard/project/_/sql) to create all tables and RLS policies.

### 4. Google Sheets (Optional)

To enable student sync from Google Forms:
1. Create a service account in [Google Cloud Console](https://console.cloud.google.com/)
2. Download the credentials as `credentials.json` and place in the project root
3. Share your Google Sheet with the service account email

### 5. Run

```bash
python admin_login.py
```

The app will be available at `http://127.0.0.1:5000`

## Project Structure

```
eventhub-demo/
├── admin_login.py          # Main Flask app (all routes & logic)
├── schema.sql              # Database schema & RLS policies
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── templates/
│   ├── index.html          # Public landing page
│   ├── event-details.html  # Public event details
│   ├── admin_login.html    # Admin login page
│   ├── admin_signup.html   # Admin registration
│   └── admin_dashboard.html# Admin dashboard (events, students, reports)
└── static/
    ├── public_styles.css   # Landing page styles
    ├── public_script.js    # Landing page JavaScript
    ├── style.css           # Admin dashboard styles
    ├── admin_login.css     # Login/signup page styles
    ├── script.js           # Admin dashboard JavaScript
    └── uploads/            # Event images (user uploads)
```
