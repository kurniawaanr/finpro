from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, inspect, delete


def create_table_banners():
    engine = get_engine()

    if not inspect(engine).has_table('banners'):
        meta = MetaData()
        banners = Table(
            'banners',
            meta,
            Column('id', String, primary_key=True),
            Column('image', String(128)),
            Column('title', String(128), unique=True)
        )
        meta.create_all(engine)
    else:
        banners = Table("banners", MetaData(bind=get_engine()), autoload=True)
        run_query(delete(banners), commit=True)
