from sqlalchemy import Table, MetaData, select, insert, update, delete
from migrations.categories import create_table_categories
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_categories()
categories = Table("categories", MetaData(
    bind=get_engine()), autoload=True)


def get_all_categories():
    return run_query(select(categories))


def duplicate_category(title):
    category = run_query(select(categories).where(
        (categories.c.title == title)))
    if len(category) != 0:
        return True

    return False


def insert_category(values):
    return run_query(insert(categories).values(values), commit=True)


def update_category_by_id(values, id):
    return run_query(update(categories).values(values).where(categories.c.id == id), commit=True)


def category_exist(id):
    categoryById = run_query(select(categories).where(
        categories.c.id == id))
    if len(categoryById) == 0:
        return False
    return True


def remove_category(id):
    return run_query(delete(categories).where(categories.c.id == id), commit=True)
