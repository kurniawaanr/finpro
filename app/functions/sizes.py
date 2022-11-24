from sqlalchemy import Table, MetaData, select, and_
from migrations.sizes import create_table_sizes
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_sizes()
sizes = Table("sizes", MetaData(bind=get_engine()), autoload=True)


def get_sizes_list(product_id):
    size = run_query(select(sizes).where(
        sizes.c.product_id == product_id))

    size_list = []

    for i in range(len(size)):
        size_list.append(size[i]["size"])

    if len(size_list) <= 1:
        size_list = size_list[0]

    return size_list


def get_size_id(product_id, size):
    size = run_query(select(sizes).where(
        and_(sizes.c.product_id == product_id, sizes.c.size == size)))
    return size[0]["id"]


def get_size_by_size_id(size_id):
    return run_query(select(sizes).where(sizes.c.id == size_id))
