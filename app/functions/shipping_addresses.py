from sqlalchemy import Table, MetaData, insert, select, update
from migrations.shipping_addresses import create_table_shipping_addresses
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_shipping_addresses()
shipping_addresses = Table("shipping_addresses", MetaData(
    bind=get_engine()), autoload=True)


def get_address_by_token(token):
    return run_query(
        select(shipping_addresses).where(shipping_addresses.c.token == token))


def shipp_ad_exist(token):
    sa = get_address_by_token(token)
    if len(sa) == 0:
        return False

    return True


def insert_sa(values):
    return run_query(insert(shipping_addresses).values(values), commit=True)


def update_sa(values, token):
    return run_query(update(shipping_addresses).values(values).where(shipping_addresses.c.token == token), commit=True)
