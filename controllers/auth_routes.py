from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import  timedelta
from fastapi.security import OAuth2PasswordRequestForm

from models import Dweller
from config.dependencies import get_session, verify_token, create_token, authenticate_user
from services import bcrypt_context
from schemas import DwellerSchema, LoginSchema
from config.settings import SECRET_KEY, ALG, ACCESS_TOKEN_DURATION
from utils.utils import is_valid_cpf

auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.post("/create_dweller")
async def create_dweller(dweller_schema : DwellerSchema, session: Session = Depends(get_session)):
    dweller = session.query(Dweller).filter(Dweller.cpf == dweller_schema.cpf).first()
    if not is_valid_cpf(dweller_schema.cpf):
        raise HTTPException(status_code=400, detail="CPF is not valid")
    if dweller:
        raise HTTPException(status_code=400, detail="Dweller already signed up")
    else:
        crypt_password = bcrypt_context.hash(dweller_schema.password)
        new_dweller = Dweller(dweller_schema.name, dweller_schema.email, dweller_schema.cpf, crypt_password, dweller_schema.active, dweller_schema.admin)
        session.add(new_dweller)
        session.commit()
        return {"log": "dweller created"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):

    user =  authenticate_user(login_schema.cpf, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or wrong information.")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user_id= user.id, token_duration=timedelta(days=3))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
    

@auth_router.post("/login-form")
async def login_form(oauth_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user =  authenticate_user(oauth_form.username, oauth_form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or wrong information.")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }
    

@auth_router.get("/refresh")
async def use_refresh_token(user: Dweller = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
    "access_token": access_token,
    "token_type": "Bearer"
    }