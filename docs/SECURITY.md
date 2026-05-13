# Security Architecture & RBAC Policy

## Security Controls
1. **Authentication**: JWT authentication with rotating refresh tokens (`rest_framework_simplejwt`). Short-lived access tokens (1 day dev / 15 mins prod).
2. **Role-Based Access Control (RBAC)**: Custom permissions enforce exact boundaries for Super Admin, College Admin, Faculty, Staff, and Student roles.
3. **Audit Trails**: Middleware intercepts mutating requests (`POST`, `PUT`, `PATCH`, `DELETE`) recording IP addresses and user actions in immutable `AuditLog` table.
4. **Data Protection**: Zero secrets committed to source control; configuration managed via environment variables.
