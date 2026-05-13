# Contributing Guidelines

## Branching & Workflow Strategy
- `main`: Production-ready releases only. Triggers deployment to AWS Production.
- `develop`: Staging & integration branch. Triggers deployment to Azure Staging.
- Feature branches: `feature/feature-name` branched off `develop`.

## Commit Conventions
Follow atomic, descriptive git commit messages:
- `feat(auth): Add JWT token refresh and RBAC permissions`
- `fix(attendance): Correct percentage calculation for excused absences`
- `test(backend): Add unit tests for department CRUD endpoints`
