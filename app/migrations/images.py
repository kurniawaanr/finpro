from utils import get_engine, run_query
from sqlalchemy import MetaData, Table, Column, String, inspect, delete


def create_table_images():
    engine = get_engine()

    if not inspect(engine).has_table('images'):
        meta = MetaData()
        images = Table(
            'images',
            meta,
            Column('product_id', String),
            Column('images_url', String(128))
        )
        meta.create_all(engine)
    else:
        images = Table("images", MetaData(bind=get_engine()), autoload=True)
        run_query(delete(images), commit=True)
