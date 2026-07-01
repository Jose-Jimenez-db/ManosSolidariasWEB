"""
Este archivo configura la conexión con la base de datos MySQL mediante
SQLAlchemy. Además, define el motor de conexión, la sesión utilizada por
los repositorios, la clase base para las entidades y la función encargada
de crear las tablas del sistema cuando sea necesario.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/manos_solidarias_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
