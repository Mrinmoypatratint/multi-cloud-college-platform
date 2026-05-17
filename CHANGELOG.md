# Changelog

All notable changes to the **Multi-Cloud College Management & Student Services Platform** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-10

### Added
- **Authentication & RBAC**: Custom Django User model supporting 5 roles (`SUPER_ADMIN`, `COLLEGE_ADMIN`, `FACULTY`, `STAFF`, `STUDENT`) with JWT Token authentication (`rest_framework_simplejwt`).
- **Academic Domain**: Department management, degree course setup, curriculum subject catalog, and faculty assignment mapping.
- **Attendance Engine**: Class session log, bulk student attendance marking, and percentage calculation analytics.
- **Timetable Engine**: Weekly lecture matrix schedule slots.
- **Notices Feed**: Role-targeted announcement feed with priority badges and pin controls.
- **Security & Audit**: Mutating request audit log middleware capturing IP addresses, HTTP methods, and status codes.
- **Reporting & Health**: Public health check endpoint (`/api/v1/reports/health/`) and dashboard KPI endpoint.
- **React Frontend**: Vite-powered React 18 SPA with light/dark theme switcher, responsive sidebar, data tables, and modal forms.
- **Containerization**: Multi-stage `Dockerfile`s for Django and React, along with Nginx reverse proxy configuration.
- **Multi-Cloud Infrastructure**: Terraform modules for AWS Production (ECS Fargate + RDS Multi-AZ) and Azure Staging/DR (App Service + PostgreSQL Flexible).
- **CI/CD Pipeline**: GitHub Actions workflow (`ci-cd.yml`) running backend/frontend tests, Bandit security scans, Docker build checks, and cloud deployments.
- **Documentation**: `README.md`, `ARCHITECTURE.md`, `DEPLOYMENT.md`, `API.md`, `SECURITY.md`, `TESTING.md`, `CONTRIBUTING.md`, `TROUBLESHOOTING.md`, `ONBOARDING.md`, and `DEVELOPMENT_TIMELINE.md`.
