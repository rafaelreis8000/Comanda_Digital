from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

db = create_engine('sqlite:///Proj_Lanches\database.db', echo = True)
Base = declarative_base()

class Lanche(Base):
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key= True)
    nome = Column(String, nullable= False)
    ingredientes = Column(String)
    valor = Column(Float, nullable= False)

    pedidos = relationship('Pedido', back_populates = 'Lanche')

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key= True)
    itens = Column(Integer, ForeignKey('lanches.id'))
    total = Column(Float, nullable= False)

    pedidos = relationship('Lanche', back_populates = 'Pedido')

Base.metadata.create_all(db)

Session = sessionmaker(bind = db)
session = Session()

x_burguer = Lanche(nome = 'X-Burguer', ingredientes = 'Pão Brioche, hambúrguer 150g, queijo cheddar e molho especial', valor = 23.90)
session.add(x_burguer)

session.commit()