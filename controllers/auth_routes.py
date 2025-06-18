from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models import Dweller
from config.dependencies import (
    get_session, verify_token, create_token, authenticate_user
)
from services import bcrypt_context
from schemas import DwellerSchema, LoginSchema
from utils.utils import Validator, CpfValidation


router = InferringRouter(prefix="/auth", tags=["auth"])

@cbv(router)
class AuthView:
    session: Session = Depends(get_session)

    @router.post("/create_dweller")
    async def create_dweller(self, dweller_schema: DwellerSchema):
        dweller = self.session.query(Dweller).filter(Dweller.cpf == dweller_schema.cpf).first()
        validator = Validator(CpfValidation())

        if not validator.perform_validation(dweller_schema.cpf):
            raise HTTPException(status_code=400, detail="CPF inválido")

        if dweller:
            raise HTTPException(status_code=400, detail="Morador já cadastrado")

        crypt_password = bcrypt_context.hash(dweller_schema.password)

        new_dweller = Dweller(
            name=dweller_schema.name,
            email=dweller_schema.email,
            cpf=dweller_schema.cpf,
            password=crypt_password,
            active=dweller_schema.active,
            admin=dweller_schema.admin
        )

        self.session.add(new_dweller)
        self.session.commit()

        return {"message": "Morador cadastrado com sucesso"}

    @router.post("/login")
    async def login(self, login_schema: LoginSchema):
        user = authenticate_user(login_schema.cpf, login_schema.password, self.session)

        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado ou informações incorretas")

        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=3))
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

    @router.post("/login-form")
    async def login_form(self, oauth_form: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(oauth_form.username, oauth_form.password, self.session)

        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado ou informações incorretas")

        access_token = create_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    @router.get("/refresh")
    async def refresh(self, user: Dweller = Depends(verify_token)):
        access_token = create_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
