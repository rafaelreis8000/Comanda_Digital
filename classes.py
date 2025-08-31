from sqlalchemy import create_engine, Integer, String, Float, Column
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///Proj_Lanches/Banco/database.db', echo = True)

Session = sessionmaker(bind = engine)
session = Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

class Lanche(BaseModel):
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    description = Column(String, nullable = False)
    value = Column(Float, nullable = False)

class Pedido(BaseModel):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key = True)
    itens = Column()