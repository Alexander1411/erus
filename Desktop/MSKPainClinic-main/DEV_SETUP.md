# Development Setup Guide

## Quick Fix for "Connection Refused" Error

### Issue 1: Wrong Port
- **You're accessing:** `127.0.0.1:5000`
- **Django runs on:** `127.0.0.1:8000` (default port)

### Issue 2: DEBUG = False
With `DEBUG = False`, the development server won't serve static files properly.

---

## Solution: Setup for Development

### Step 1: Create/Update `.env` File

Create a `.env` file in the project root with:

```env
# For DEVELOPMENT - set to True
DEBUG=True

# For PRODUCTION - set to False
# DEBUG=False

SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,mskpainclinic.onrender.com
YANDEX_MAPS_API_KEY=your-api-key-if-needed
```

### Step 2: Start the Development Server

**On Windows (PowerShell):**
```powershell
python manage.py runserver
```

**Or specify port 8000 explicitly:**
```powershell
python manage.py runserver 8000
```

**Or if you want to use port 5000:**
```powershell
python manage.py runserver 5000
```

### Step 3: Access the Website

- **Default:** http://127.0.0.1:8000/
- **Or:** http://localhost:8000/
- **If using port 5000:** http://127.0.0.1:5000/

---

## Common Issues

### "ModuleNotFoundError: No module named 'dotenv'"
**Fix:**
```powershell
pip install python-dotenv
```

### "DisallowedHost" Error
**Fix:** Make sure `127.0.0.1` and `localhost` are in your `ALLOWED_HOSTS` in `.env`

### Static Files Not Loading
**Fix:** 
1. Set `DEBUG=True` in `.env`
2. Run: `python manage.py collectstatic` (if needed)

### Server Already Running
**Fix:** 
- Check if another terminal has the server running
- Or use a different port: `python manage.py runserver 8001`

---

## Development vs Production

| Setting | Development | Production |
|---------|-------------|------------|
| DEBUG | `True` | `False` |
| Port | 8000 (default) | 80/443 |
| Static Files | Auto-served | Need collectstatic |
| Error Pages | Detailed | Generic |

---

## Quick Commands

```bash
# Start server (default port 8000)
python manage.py runserver

# Start on specific port
python manage.py runserver 5000

# Start and allow external connections
python manage.py runserver 0.0.0.0:8000

# Check for errors
python manage.py check
```

---

**After setting DEBUG=True in .env, restart your server!**

