from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, inspect, delete


def create_table_shipping_addresses():
    engine = get_engine()

    if not inspect(engine).has_table('shipping_addresses'):
        meta = MetaData()
        shipping_addresses = Table(
            'shipping_addresses',
            meta,
            Column('id', String, primary_key=True),
            Column('name', String(128)),
            Column('address', String(128)),
            Column('city', String(64)),
            Column('token', String)
        )
        meta.create_all(engine)
    else:
        shipping_addresses = Table("shipping_addresses", MetaData(
            bind=get_engine()), autoload=True)
        run_query(delete(shipping_addresses), commit=True)
