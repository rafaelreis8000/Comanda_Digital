from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
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
    
    def cadastrar_cliente(nome, sobrenome, telefone):
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

    def criar_lanche(nome, descricao, valor):
        lanche = Lanche(nome = nome, descricao = descricao, valor = valor)
        session.add(lanche)
        session.commit()


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column('id', Integer, primary_key = True, nullable = False)
    cliente = Column('cliente', ForeignKey('clientes.id'))
    data = Column('data', DateTime)

    def __init__(self, cliente, data):
        self.cliente = cliente
        self.data = data
    
    def fazer_pedido(cliente, data = datetime.today()):
        pedido = Pedido(cliente = cliente, data = data)
        session.add(pedido)
        session.commit()


class Pedido_Lanche(Base):
    __tablename__ = 'pedidos_lanche'

    id = Column('id', Integer, primary_key = True)
    quantidade = Column('quantidade', Integer, nullable = False)

    def __init__(self, id, quantidade):
        self.id = id
        self.quantidade = quantidade

    def mostrar_pedido(id, quantidade):
        pedido_lanche = Pedido_Lanche(id = "'pedido.id','lanche.id'", quantidade = 0)
        session.add(pedido_lanche)
        session.commit()


Base.metadata.create_all(bind = db)