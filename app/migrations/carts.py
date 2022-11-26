from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, Integer, inspect, delete


def create_table_carts():
    engine = get_engine()

    if not inspect(engine).has_table('carts'):
        meta = MetaData()
        carts = Table(
            'carts',
            meta,
            Column('id', String, primary_key=True),
            Column('quantity', Integer),
            Column('token', String),
            Column('shipping_method', String(64)),
            Column('size_id', String(128), unique=True),
            Column('created_at', String(128)),
            Column('status', String(128)),
            Column('total_price', Integer)
        )
        meta.create_all(engine)
    else:
        carts = Table("carts", MetaData(bind=get_engine()), autoload=True)
        run_query(delete(carts), commit=True)
