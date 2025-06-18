from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models import Dweller, DeliveryGuy, Uber, Guest
from config.dependencies import (
    get_session, verify_token, create_token, authenticate_user
)
from services import bcrypt_context
from schemas import DwellerSchema, LoginSchema
from utils.utils import Validator, CpfValidation

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/list")
async def list_requests(id_pedido: int, session: Session = Depends(get_session), user: Dweller = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Access Denied: Admins only")
    