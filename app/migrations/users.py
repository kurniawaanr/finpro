from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, Integer, inspect, delete


def create_table_users():
    engine = get_engine()

    if not inspect(engine).has_table('users'):
        meta = MetaData()
        users = Table(
            'users',
            meta,
            Column('id', String, primary_key=True),
            Column('name', String(128), unique=True),
            Column('email', String(128), unique=True),
            Column('password', String(128)),
            Column('phone_number', String(128), unique=True),
            Column('token', String(64), unique=True),
            Column('type', String(12)),
            Column('balance', Integer)
        )
        meta.create_all(engine)
    else:
        users = Table("users", MetaData(bind=get_engine()), autoload=True)
        run_query(delete(users), commit=True)
