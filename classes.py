from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

db = create_engine('sqlite:///D:\GitHub\Proj_Lanches/banco.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    nome = Column('nome', String, nullable = False)
    sobrenome = Column('sobrenome', String, nullable = False)
    telefone = Column('telefone', Integer, nullable = False)

    def __init__(self, nome, sobrenome, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
    
    def cadastrar_cliente(self, nome, sobrenome, telefone):
        cliente = Cliente(nome = nome, sobrenome = sobrenome, telefone = telefone)
        session.add(cliente)
        session.commit()


class Lanche(Base):
    __tablename__ = 'lanches'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    nome = Column('nome', String, nullable = False)
    descricao = Column('descrição', String)
    valor = Column('valor', Float, nullable = False)

    def __init__(self, nome, descricao, valor):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

    def criar_lanche(self, nome, descricao, valor):
        lanche = Lanche(nome = nome, descricao = descricao, valor = valor)
        session.add(lanche)
        session.commit()


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column('id', Integer, primary_key = True, nullable = False)
    cliente = Column('cliente', ForeignKey('clientes.id'))
    data = Column('data',)##########################################

    def __init__(self, cliente, data):
        self.cliente = cliente
        self.data = data
    
    def fazer_pedido(self, cliente, data):##########################
        pedido = Pedido(cliente, data)##############################
        session.add(pedido)
        session.commit()

Base.metadata.create_all(bind = db)