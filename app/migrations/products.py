from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, Integer, inspect, delete


def create_table_products():
    engine = get_engine()

    if not inspect(engine).has_table('products'):
        meta = MetaData()
        products = Table(
            'products',
            meta,
            Column('id', String, primary_key=True),
            Column('title', String(128), unique=True),
            Column('price', Integer),
            Column('category_id', String(128)),
            Column('product_detail', String(128)),
            Column('condition', String(128))
        )
        meta.create_all(engine)
    else:
        products = Table("products", MetaData(
            bind=get_engine()), autoload=True)
        run_query(delete(products), commit=True)
