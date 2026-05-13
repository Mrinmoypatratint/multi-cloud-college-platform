# System Architecture & SOLID Blueprint

## Overview
The **Multi-Cloud College Management & Student Services Platform** follows a clean, modular, decoupled multi-tier architecture.

```
+-------------------------------------------------------------+
|                      Client Layer                          |
|               React 18 SPA (Vite + Enterprise CSS)           |
+-------------------------------------------------------------+
                              |
                     HTTPS / REST Requests
                              v
+-------------------------------------------------------------+
|                     Edge / Reverse Proxy                    |
|                        Nginx Proxy                          |
+-------------------------------------------------------------+
                              |
                     WSGI Gunicorn Requests
                              v
+-------------------------------------------------------------+
|                     Backend API Layer                       |
|           Django 5.1 REST Framework (Modular Apps)          |
|  - apps.users (RBAC Auth, Profiles)                         |
|  - apps.academic (Depts, Courses, Subjects)                 |
|  - apps.attendance (Session & Bulk Record Logging)          |
|  - apps.timetable (Weekly Matrix Slots)                     |
|  - apps.notices (Targeted Feed)                             |
|  - apps.audit (Middleware & Activity Trail)                 |
|  - apps.reports (Health & Analytics Summary)               |
+-------------------------------------------------------------+
                              |
                      Database Queries
                              v
+-------------------------------------------------------------+
|                     Persistence Layer                       |
|                  PostgreSQL 16 Multi-AZ DB                  |
+-------------------------------------------------------------+
```

## Architectural Principles
1. **SOLID Principles**:
   - **Single Responsibility Principle**: Distinct domain apps for Users, Academic, Attendance, Timetable, Notices, and Audit.
   - **Open/Closed Principle**: Base permission classes (`IsCollegeAdmin`, `IsFaculty`) extensible without modifying core REST viewsets.
   - **Liskov Substitution**: Custom user model inherits `AbstractUser` preserving all standard Django auth contracts.
   - **Interface Segregation**: Focused serializers for minimal reads (`DepartmentMinimalSerializer`) vs full detail reads.
   - **Dependency Inversion**: Service layers depend on abstract Model ORM and standard DRF serializer interfaces.

2. **Security & Secrets Management**:
   - Environment variables loaded via `python-dotenv`.
   - Zero hardcoded secrets in repository.
