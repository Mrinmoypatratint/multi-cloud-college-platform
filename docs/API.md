# API Specification & Endpoint Documentation

## Overview
All API endpoints follow RESTful standards under `/api/v1/` prefix and return standard JSON formats:
```json
{
  "success": true,
  "message": "Description of outcome",
  "data": {},
  "errors": {}
}
```

---

## Endpoint Catalog

### Authentication
- `POST /api/v1/auth/login/` - Obtain JWT access and refresh token pair + full user profile payload.
- `POST /api/v1/auth/refresh/` - Refresh expired access token.
- `GET /api/v1/auth/me/` - Retrieve authenticated user profile.

### User Management
- `GET /api/v1/auth/users/` - Search and list users (Filter by role, department, name).
- `POST /api/v1/auth/users/` - Create student, faculty, or staff account (College Admin only).

### Academic Catalog
- `GET /api/v1/academic/departments/` - List departments.
- `GET /api/v1/academic/courses/` - List courses and degree programs.
- `GET /api/v1/academic/subjects/` - List curriculum subjects.

### Attendance Portal
- `POST /api/v1/attendance/bulk/` - Bulk mark student attendance for a class session.
- `GET /api/v1/attendance/summary/` - Retrieve attendance breakdown and percentage calculation.

### Timetable & Notices
- `GET /api/v1/timetable/slots/` - Retrieve weekly timetable schedule matrix.
- `GET /api/v1/notices/` - List filterable notice feed for user role.

### System & Health
- `GET /api/v1/reports/health/` - Public health check (Database connectivity & system status).
- `GET /api/v1/reports/dashboard/` - Dashboard KPI statistics.
- `GET /api/v1/audit/logs/` - Immutable security audit trail (Admins only).
