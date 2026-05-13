# Testing & Verification Guide

## Test Suites Overview
- **Backend Tests**: Built with Django TestCase / Pytest covering auth, academic, attendance, notices, reports, and RBAC permissions.
- **Frontend Tests**: Built with Vitest & React Testing Library verifying component rendering and AuthContext.

## Execution Commands
```bash
# Run Backend Tests
python backend/manage.py test tests

# Run Frontend Component Tests
cd frontend
npm run test
```
