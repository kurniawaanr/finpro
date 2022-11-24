from sqlalchemy import Table, MetaData, select
from migrations.banners import create_table_banners
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_banners()
banners = Table("banners", MetaData(bind=get_engine()), autoload=True)


def get_all_banners():
    return run_query(select(banners))
