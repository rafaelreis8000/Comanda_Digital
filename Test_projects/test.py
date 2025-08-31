from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, bindparam, ForeignKey, func
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///Proj_Lanches/Test_projects/test.db', echo = True)

meta = MetaData()

people = Table(
    'people',
    meta,
    Column('id', Integer, primary_key = True),
    Column('name', String, nullable = False),
    Column('age', Integer)
)

things = Table(
    'table',
    meta,
    Column('id', Integer, primary_key = True),
    Column('description', String, nullable = False),
    Column('value', Float, nullable = False),
    Column('owner', Integer, ForeignKey('people.id')) #The ID from a person relates to this table
    #One person can own many things, but one thing can only be owned by a person
)

meta.create_all(engine)
conn = engine.connect()

def add_people(name, age):
    insert_statement = insert(people).values(name = name, age = age)
    result = conn.execute(insert_statement)
    conn.commit()

def find_people(id):
    select_statement = people.select().where(people.c.id == id)
    result = conn.execute(select_statement)
    for i in result.fetchall():
        print(i)

def delete_people(id):
    delete_statement = people.delete().where(people.c.id == id)
    result = conn.execute(delete_statement)
    conn.commit()

def add_things(desc, value, owner):
    insert_things = things.insert().values(description = desc, value = value, owner = owner)
    conn.execute(insert_things)
    conn.commit()

def join(): #shows only those who own anything
    join_statement = people.join(things, people.c.id == things.c.owner)
    select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement)
    result = conn.execute(select_statement)
    for i in result.fetchall():
        print(i)

def group():
    group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner)
    result = conn.execute(group_by_statement)
    
    for i in result.fetchall():
        print(i)