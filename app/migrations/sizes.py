from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, CHAR, inspect, delete


def create_table_sizes():
    engine = get_engine()

    if not inspect(engine).has_table('sizes'):
        meta = MetaData()
        sizes = Table(
            'sizes',
            meta,
            Column('id', String, primary_key=True),
            Column('product_id', String(128)),
            Column('size', CHAR)
        )
        meta.create_all(engine)
    else:
        sizes = Table("sizes", MetaData(bind=get_engine()), autoload=True)
        run_query(delete(sizes), commit=True)
