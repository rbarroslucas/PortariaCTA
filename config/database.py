from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from config.settings import DATABASE_URL

db = create_engine(DATABASE_URL, echo=True, client_encoding='utf8')
Base = declarative_base()