from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from config.database import db
from models import Dweller
from services import bcrypt_context
from jose import jwt, JWTError
from config.settings import SECRET_KEY, ALG, ACCESS_TOKEN_DURATION
from services import oauth2_schema

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def get_admin(session):
    admins = session.query(Dweller).filter(Dweller.admin == True).all()
    dic = {}
    for admin in admins:
        dic.update({"admin_{}".format(admin.id): {
            "name": admin.name,
            "email": admin.email,
            "cpf": admin.cpf,
            "id": admin.id
        }})
    return dic

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALG)
        user_id = int(dic_info.get("sub"))
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = session.query(Dweller).filter(Dweller.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized - User not found")
    return user

def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_DURATION)):
    exp_date = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": exp_date}
    jwt_token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALG)
    return jwt_token
    

def authenticate_user(username: str, password: str, session: Session):
    user = session.query(Dweller).filter(Dweller.cpf == username).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

