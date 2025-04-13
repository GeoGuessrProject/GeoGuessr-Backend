from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import User
from dotenv import load_dotenv
from jwt_handler import create_access_token, hash_password, verify_password

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def index():
    return {"message": "Connected"}

# Create DB tables
from db import Base
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register endpoint
@app.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        email = body.get("email")
        country = body.get("country")
        age = body.get("age")

        if not all([username, password, email, country, age]):
            raise HTTPException(status_code=400, detail="All fields are required")

        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_pw = hash_password(password)

        new_user = User(
            username=username,
            password=hashed_pw,
            email=email,
            country=country,
            age=age
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Registration successful", "username": new_user.username}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Login endpoint
@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")

        if not all([username, password]):
            raise HTTPException(status_code=400, detail="Username and password are required")

        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer", "username": user.username}    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

