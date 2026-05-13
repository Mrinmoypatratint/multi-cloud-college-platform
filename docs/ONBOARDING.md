# Developer Onboarding Guide

Welcome to the **Multi-Cloud College Management & Student Services Platform** engineering team!

## 1. Initial Setup Checklist
- [ ] Clone repository: `git clone <repo-url>`
- [ ] Install Python 3.11+ and Node.js v20+
- [ ] Create Python virtual environment and install requirements:
      `python -m venv venv && .\venv\Scripts\pip install -r backend/requirements.txt`
- [ ] Run Django migrations and seed data:
      `python backend/manage.py migrate && python backend/manage.py seed_data`
- [ ] Install React dependencies:
      `cd frontend && npm install`
- [ ] Start development servers:
      Backend: `python backend/manage.py runserver` (Port 8000)
      Frontend: `npm run dev` (Port 3000)
- [ ] Test login with demo account `superadmin` / `admin123`
