from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import os

from config import settings

app = FastAPI()

# ✅ CORS Middleware - MUST be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy User Database
fake_user_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("123456")
    }
}

# ===== API ENDPOINTS =====

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/")
def home():
    """Home endpoint"""
    return {
        "message": "FastAPI JWT Authentication Running",
        "docs": "/docs",
        "ui": "/ui"
    }

@app.get("/ui")
def ui():
    """Serve the HTML UI"""
    return FileResponse("templates/index.html", media_type="text/html")

# ===== AUTHENTICATION FUNCTIONS =====

def verify_password(plain_password, hashed_password):
    """Verify plain password against hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== LOGIN ENDPOINT =====

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"[LOGIN] Username: {form_data.username}")
    
    user = fake_user_db.get(form_data.username)

    if not user:
        print(f"[LOGIN] User not found: {form_data.username}")
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user["hashed_password"]):
        print(f"[LOGIN] Wrong password for: {form_data.username}")
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_token({"sub": form_data.username})
    print(f"[LOGIN] Token generated for: {form_data.username}")

    # ✅ Return proper JSON response
    return JSONResponse(
        status_code=200,
        content={
            "access_token": access_token,
            "token_type": "bearer"
        }
    )

# ===== PROTECTED ENDPOINT =====

@app.get("/protected")
def protected_route(username: str = Depends(verify_token)):
    print(f"[PROTECTED] Accessed by: {username}")
    
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Hello {username}, this is protected data!",
            "user": username
        }
    )

# ===== ERROR HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )