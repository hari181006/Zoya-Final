import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, SupportRequest
from ..auth import create_token, decode_token

router=APIRouter(prefix="/api/admin",tags=["Admin"])
bearer=HTTPBearer(auto_error=False)

def require_admin(credentials: HTTPAuthorizationCredentials=Depends(bearer)):
    if not credentials: raise HTTPException(401,"Admin login required")
    try: p=decode_token(credentials.credentials)
    except Exception: raise HTTPException(401,"Invalid or expired admin token")
    if p.get("role")!="admin": raise HTTPException(403,"Admin access required")
    return p

@router.post("/login")
def admin_login(data: dict):
    if data.get("user_id") != os.getenv("ADMIN_USER_ID","admin") or data.get("password") != os.getenv("ADMIN_PASSWORD","ZoyaAdmin@2026"):
        raise HTTPException(401,"Invalid admin credentials")
    return {"message":"Admin login successful","access_token":create_token(0,"admin"),"role":"admin"}

@router.get("/users")
def users(_:dict=Depends(require_admin), db:Session=Depends(get_db)):
    rows=db.query(User).order_by(User.id.desc()).all()
    return [{"id":u.id,"full_name":u.full_name,"mobile":u.mobile,"email":u.email,"is_active":u.is_active,"created_at":u.created_at.isoformat()} for u in rows]

@router.delete("/users/{mobile}")
def delete_user(mobile:str, _:dict=Depends(require_admin), db:Session=Depends(get_db)):
    u=db.query(User).filter(User.mobile==mobile).first()
    if not u: raise HTTPException(404,"User not found")
    db.delete(u); db.commit(); return {"message":"User deleted"}

@router.get("/support-requests")
def support_requests(_:dict=Depends(require_admin), db:Session=Depends(get_db)):
    rows=db.query(SupportRequest).order_by(SupportRequest.id.asc()).all()
    return [{"id":r.id,"name":r.name,"mobile":r.mobile,"message":r.message,"read":r.read,"createdAt":r.created_at.isoformat()} for r in rows]

@router.put("/support-requests/{request_id}/read")
def mark_read(request_id:int, _:dict=Depends(require_admin), db:Session=Depends(get_db)):
    r=db.get(SupportRequest,request_id)
    if not r: raise HTTPException(404,"Request not found")
    r.read=True; db.commit(); return {"message":"Marked as read"}
