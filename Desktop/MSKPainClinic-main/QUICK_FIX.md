# Quick Fix for SSL Error

## The Problem
Your browser is trying to use HTTPS, but Django dev server only supports HTTP.

## Solution (3 Steps)

### Step 1: Clear Browser Cache/HSTS
The browser might have cached HTTPS redirect. Try:

1. **Clear HSTS for localhost:**
   - Go to: `chrome://net-internals/#hsts`
   - In "Delete domain security policies", enter: `127.0.0.1`
   - Click "Delete"

2. **Or use Incognito/Private window** (Ctrl+Shift+N)

### Step 2: Make Sure Server is Running

Open PowerShell in your project folder and run:

```powershell
python manage.py runserver 5000
```

You should see:
```
Starting development server at http://127.0.0.1:5000/
```

### Step 3: Access with HTTP (not HTTPS)

**Important:** Use `http://` not `https://`

✅ **Correct:** http://127.0.0.1:5000/  
❌ **Wrong:** https://127.0.0.1:5000/

---

## Alternative: Use Port 8000 (Default)

If port 5000 still has issues:

```powershell
python manage.py runserver
```

Then access: **http://127.0.0.1:8000/**

---

## If Still Not Working

1. **Check if server is actually running:**
   - Look for "Starting development server" message
   - If you see errors, share them

2. **Try different browser:**
   - Edge, Firefox, etc.

3. **Check firewall:**
   - Windows might be blocking the port

4. **Verify DEBUG is True:**
   - The code now defaults to DEBUG=True
   - But you can also create `.env` file with: `DEBUG=True`

---

## Quick Test Command

```powershell
# Start server
python manage.py runserver 5000

# In another terminal, test connection
curl http://127.0.0.1:5000/
```

