from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

db = create_engine('sqlite:///banco.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()

class PedidoLanche(Base):
    '''
    POR - Tabela de relacionamentos. Recebe a ID do pedido, a ID de cada lanche e suas quantidades. Essas informações
    são geradas na tabela Pedido. Baseado na quantidade de cada lanche e no preço de
    cada um, mostra o valor total do pedido

    ENG - Relationship Table. Recieves the order's ID, each burguer's ID and its quantities. These information are
    generated at Pedido's(Order) Table. Based on each burguer's quantity and its prices, shows the total cost of the order
    '''
    __tablename__ = 'pedido_lanches'
    id = Column(Integer, primary_key = True)
    pedido_id = Column(ForeignKey('pedidos.id'))
    lanche_id = Column(ForeignKey('lanches.id'))
    quantidade = Column(Integer, nullable = False, default = 1)
    total = Column(Float, nullable = False, default = 0)

class Lanche(Base):
    '''
    POR - Tabela Lanche. Cadastra os lanches do cardápio no sistema. Possui uma relação de vários para
    vários com Pedido, permitindo que vários pedidos possuam vários lanches.
    
    ENG - Table Lanche(Burguer). Registers the burguers from the menu. Has a relationship of many to many
    with Pedido (Order), allowing many orders to have many burguers
    '''
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    valor = Column(Float, nullable = False)
    descricao = Column(String)
    pedidos = relationship('Pedido', secondary = 'pedido_lanches', back_populates = 'lanches')

    def __init__(self, nome, valor, descricao):
        self.nome = nome
        self.valor = valor
        self.descricao = descricao

    def cadastrar_lanche(nome, valor, descricao = ''):
        session.add(Lanche(nome = nome, valor = valor, descricao = descricao))
        session.commit()

class Pedido(Base):
    '''
    POR - Tabela que inicia os pedidos. Recebe o ID do cliente que fez o pedido, os lanches e a
    quantidade de cada um. Possui uma relação de vários para vários com Lanche, permitindo que vários
    pedidos possam conter vários lanches.

    ENG - Table that starts an order. Recieves the ID from the client owner of the order, the burguers
    ordered and the quantity of each one of them. It has a many to many relationship with Lanches (Burguers),
    allowing many Orders to have many Burguers.
    '''
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key = True)
    data = Column(DateTime, nullable = False, default = datetime.today())
    cliente = Column(ForeignKey('clientes.id'))
    lanches = relationship('Lanche', secondary = 'pedido_lanches', back_populates = 'pedidos')

    def __init__(self, cliente, lanches):
        self.cliente = cliente
        self.lanches = lanches

    def fazer_pedido(cliente, lancheid_quantidade):
        '''
        POR - Os lanches são inseridos em forma de dicionário. Cada par de chave-valor corresponde a um lanche.
        As chaves são o ID do lanche, cadastrado previamente na tabela Lanches. Já os valores são a quantidade
        de cada lanche pedido.

        ENG - All burguers are inserted via Dictionary. Each key-value pair is equal to a burguer.
        keys are equal to the burguer's ID, registered before at Lanches(Burguers) Table. The values are equal
        to the quantity of each burguer ordered.
        '''
        pedido = Pedido(cliente = cliente, lanches = [])
        session.add(pedido)
        session.flush()

        total_pedido = 0

        for lanche_id, qtd in lancheid_quantidade.items():
            lanche = session.query(Lanche).get(lanche_id)
            total_pedido += (lanche.valor * qtd)
            pedido_lanche = PedidoLanche(
                pedido_id = pedido.id,
                lanche_id = lanche.id,
                quantidade = qtd,
                total = total_pedido
            )
            session.add(pedido_lanche)
        session.commit()

class Cliente(Base):
    '''
    POR - Tabela destinada ao cadastro de clientes. Cada cliente possui seu próprio ID,
    que será utilizado na manipulação das tabelas de Pedido e PedidoLanche

    ENG - Table reserved to register clients. Each client has its own ID, which is used
    to manipulate the tables Pedido and PedidoLanche (Order, BurguerOrder)
    '''
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    sobrenome = Column(String, nullable = False)
    telefone = Column(Integer, nullable = False)

    def __init__(self, nome, sobrenome, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone

    def cadastrar_cliente(nome, sobrenome, telefone):
        session.add(Cliente(nome = nome, sobrenome = sobrenome, telefone = telefone))
        session.commit()

Base.metadata.create_all(bind = db)

def testar_cadastro():
    Cliente.cadastrar_cliente('Giuseppe', 'Cadura', 12999887675)
    Cliente.cadastrar_cliente('Pp', 'Marcondes', 1199876452)

    Lanche.cadastrar_lanche('X-Burguer', 23.90)
    Lanche.cadastrar_lanche('X-Bacon', 27.90)

    Pedido.fazer_pedido(1, {1: 2, 2: 1})
    Pedido.fazer_pedido(2, {2: 5})