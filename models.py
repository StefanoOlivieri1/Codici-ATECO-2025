from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class CodeAteco(Base):
    __tablename__ = 'codici_ateco'
    
    codice = Column(String, primary_key=True)
    descrizione = Column(String, nullable=False)
    sezione = Column(String, nullable=False)
    divisione = Column(String, nullable=False)

    def __repr__(self):
        return f"<CodeAteco(codice='{self.codice}', descrizione='{self.descrizione}')>"

# Configurazione del database
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
