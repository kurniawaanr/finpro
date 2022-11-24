from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, inspect, delete


def create_table_categories():
    engine = get_engine()

    if not inspect(engine).has_table('categories'):
        meta = MetaData()
        categories = Table(
            'categories',
            meta,
            Column('id', String, primary_key=True),
            Column('image', String(128)),
            Column('title', String(128), unique=True)
        )
        meta.create_all(engine)
    else:
        categories = Table("categories", MetaData(
            bind=get_engine()), autoload=True)
        run_query(delete(categories), commit=True)
