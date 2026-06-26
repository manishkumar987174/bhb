# FastAPI JWT Login - Setup Guide

## 📁 Project Structure

```
your-project/
├── main.py              (Replace with main_fixed.py content)
├── config.py            (Keep as is)
├── .env                 (Create new)
├── requirements.txt     (Create new)
├── templates/
│   └── index.html       (Create new)
└── static/              (Optional, can be empty)
```

---

## 🚀 Step-by-Step Setup

### 1️⃣ Create Project Directory
```bash
mkdir fastapi-jwt-login
cd fastapi-jwt-login
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Create `requirements.txt`
```
fastapi==0.104.1
uvicorn==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic-settings==2.1.0
python-multipart==0.0.6
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Create Folders
```bash
mkdir templates
mkdir static
```

### 6️⃣ Create Files

**`config.py`:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
```

**`.env`:**
```
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**`templates/index.html`:** (Use the HTML content provided)

**`main.py`:** (Use the main_fixed.py content provided)

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

Output should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🧪 Testing

### Option 1: Web UI
1. Open browser: **http://localhost:8000/ui**
2. Username: `admin`
3. Password: `123456`
4. Click **Login**

### Option 2: Swagger Docs
1. Open: **http://localhost:8000/docs**
2. Click on `/login` endpoint
3. Click **Try it out**
4. Enter username & password
5. Execute

### Option 3: cURL
```bash
# Login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456"

# Response:
# {"access_token":"eyJhbGc...","token_type":"bearer"}

# Copy the token and use it:
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🐛 Troubleshooting

### Error 405: Method Not Allowed
- Make sure you're accessing `/ui` (GET request)
- Login endpoint must receive POST request
- Check browser console for exact endpoint and method being used

### Error: Directory 'templates' does not exist
```bash
mkdir templates
mkdir static
```

### Error: "Unexpected end of JSON input"
- Server is not returning JSON
- Check the `/login` endpoint is being called correctly
- Open browser **Console** (F12) to see actual errors

### Error 401: Invalid token
- Token has expired (default: 30 minutes)
- Token is corrupted or not sent correctly
- Secret key doesn't match

### Can't connect to server
- Make sure uvicorn is running: `uvicorn main:app --reload`
- Check port 8000 is not in use
- Try different port: `uvicorn main:app --reload --port 8001`

---

## 📝 Key Changes from Original

✅ Removed Jinja2Templates (causes 405 errors)  
✅ Using FileResponse instead  
✅ Better error logging and messages  
✅ Console logging for debugging  
✅ CORS enabled for all origins  
✅ Better error handling in JavaScript  
✅ Inline CSS (no separate stylesheet needed)  

---

## 💡 Important Notes

- **Default credentials**: Username: `admin`, Password: `123456`
- **Secret key**: Change `SECRET_KEY` in `.env` for production
- **Token expires**: After 30 minutes (configurable)
- **CORS**: Currently allows all origins (fine for development)
- **Password**: Hashed with bcrypt

---

## 🔄 Development Workflow

1. Make changes to code
2. `uvicorn` will auto-reload
3. Refresh browser (F5)
4. Check browser console (F12) for errors
5. Check terminal for server-side logs

---

## ✅ Everything Working?

If you see:
- ✅ Login Successful! 
- ✅ Protected Data showing your username
- ✅ Logout clears the token

**You're all set!** 🎉