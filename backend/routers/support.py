from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import SupportRequest
from ..schemas import SupportRequestIn
from .auth import current_user

router=APIRouter(prefix="/api",tags=["Support"])
@router.post("/support")
def create_support(data:SupportRequestIn, user=Depends(current_user), db:Session=Depends(get_db)):
    r=SupportRequest(name=data.name,mobile=data.mobile,message=data.message)
    db.add(r); db.commit(); db.refresh(r); return {"message":"Support request saved","id":r.id}
