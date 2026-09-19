from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest
from ..auth import hash_password, verify_password, create_token, decode_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
bearer = HTTPBearer(auto_error=False)

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials: raise HTTPException(401, "Login required")
    try: payload=decode_token(credentials.credentials); uid=int(payload["sub"])
    except Exception: raise HTTPException(401, "Invalid or expired token")
    user=db.get(User, uid)
    if not user or not user.is_active: raise HTTPException(401, "User not found or inactive")
    return user

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    email=str(data.email).lower()
    if db.query(User).filter(or_(User.mobile==data.mobile, User.email==email)).first():
        raise HTTPException(409, "Mobile number or email already registered")
    user=User(full_name=data.full_name.strip(), mobile=data.mobile, email=email, password_hash=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"message":"Registration successful", "user":{"id":user.id,"full_name":user.full_name,"mobile":user.mobile,"email":user.email}}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.mobile==data.mobile).first()
    if not user or not user.is_active or not verify_password(data.password,user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid mobile number or password")
    return {"message":"Login successful","access_token":create_token(user.id),"token_type":"bearer","user":{"id":user.id,"full_name":user.full_name,"mobile":user.mobile,"email":user.email,"district":user.district,"address":user.address}}

@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"id":user.id,"full_name":user.full_name,"mobile":user.mobile,"email":user.email,"district":user.district,"address":user.address}

@router.put("/me")
def update_me(data: dict, user: User = Depends(current_user), db: Session = Depends(get_db)):
    user.full_name=str(data.get("full_name",user.full_name)).strip()
    user.email=str(data.get("email",user.email)).lower()
    user.district=str(data.get("district", ""))
    user.address=str(data.get("address", ""))
    db.commit(); db.refresh(user)
    return {"message":"Profile updated successfully"}
