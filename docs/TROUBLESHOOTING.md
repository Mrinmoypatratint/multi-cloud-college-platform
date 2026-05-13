# Troubleshooting Guide

## Common Issues & Solutions

### 1. Database Migration Inconsistency
**Issue**: `InconsistentMigrationHistory` error when switching custom user models.  
**Fix**: Reset SQLite development database:
```bash
rm backend/db.sqlite3
python backend/manage.py migrate
python backend/manage.py seed_data
```

### 2. Vite Windows Path Resolution
**Issue**: Script resolution errors when folder path contains spaces or ampersands (`&`).  
**Fix**: Execute node directly or wrap path in quotes:
```bash
node node_modules/vite/bin/vite.js build
```

### 3. CORS Error on API Calls
**Issue**: `Access to XMLHttpRequest at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`.  
**Fix**: Verify `django-cors-headers` is listed in `INSTALLED_APPS` and `MIDDLEWARE` in `config/settings.py`.
