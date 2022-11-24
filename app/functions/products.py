from sqlalchemy import Table, MetaData, select, insert, update, delete, desc, asc, and_
from migrations.products import create_table_products
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_products()
products = Table("products", MetaData(bind=get_engine()), autoload=True)


def valid_product(category_id, title):
    valid = run_query(select(products).where(
        and_(products.c.category_id == category_id, products.c.title == title)))

    if len(valid) == 0:
        return False

    return True


def get_product_list(condition, title, category_id, price, page, page_size, sort_by):
    if sort_by == "price a_z":
        sort_by = asc(products.c.price)
    else:
        sort_by = desc(products.c.price)

    return run_query(select(products).where(and_(products.c.condition == condition, products.c.title == title, products.c.category_id == category_id, products.c.price >= int(price))).limit(int(page)*int(page_size)).order_by(sort_by))


def get_product_by_id(id):
    return run_query(select(products).where(products.c.id == id))


def insert_product(values):
    return run_query(insert(products).values(values), commit=True)


def update_products(values, product_id):
    return run_query(update(products).values(values).where(products.c.id == product_id), commit=True)


def delete_product_category(category_id):
    return run_query(update(products).values({"category_id": "NULL"}).where(products.c.category_id == category_id), commit=True)


def remove_product(product_id):
    return run_query(delete(products).where(products.c.id == product_id), commit=True)


def duplicate_product(title, category_id, condition):
    product = run_query(select(products).where(and_(products.c.title == title,
                                                    products.c.category_id == category_id, products.c.condition == condition)))

    if len(product) == 0:
        return False

    return True
