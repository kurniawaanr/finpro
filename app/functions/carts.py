from sqlalchemy import Table, MetaData, select, insert, update, delete, and_, asc, desc
from migrations.carts import create_table_carts
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_carts()
carts = Table("carts", MetaData(bind=get_engine()), autoload=True)


def duplicate_product(size_id, token):
    cart = run_query(select(carts).where(and_(
        carts.c.size_id == size_id, carts.c.token == token, carts.c.status == "cart")))

    if len(cart) == 0:
        return False

    return True


def insert_carts(values):
    return run_query(insert(carts).values(values), commit=True)


def update_quantity(quantity, token, size_id):
    cart = run_query(select(carts).where(and_(
        carts.c.size_id == size_id, carts.c.token == token, carts.c.status == "cart")))
    return run_query(update(carts).values({"quantity": cart[0]["quantity"]+quantity}).where(and_(carts.c.token == token, carts.c.size_id == size_id, carts.c.status == "cart")), commit=True)


def get_cart_by_token(status, token):
    if status == "cart":
        return run_query(select(carts).where(and_(carts.c.token == token, carts.c.status == status)))
    else:
        return run_query(select(carts).where(and_(carts.c.token == token, carts.c.status != "cart")))


def empty_cart(token):
    cart = get_cart_by_token("cart", token)

    if len(cart) == 0:
        return True

    return False


def get_ship_price(shipping_method, total_price):
    if shipping_method == "regular" or shipping_method == "same day":
        if total_price < 200000:
            shipping_price = 0.15 * total_price
        else:
            shipping_price = 0.2 * total_price

    elif shipping_method == "next day":
        if total_price < 300000:
            shipping_price = 0.2 * total_price
        else:
            shipping_price = 0.25 * total_price

    return int(shipping_price)


def update_carts(values, id):
    return run_query(update(carts).values(values).where(carts.c.id == id), commit=True)


def delete_cart(cart_id):
    return run_query(delete(carts).where(carts.c.id == cart_id), commit=True)


def get_order_by_param(sort_by, page, page_size):
    if sort_by == "price a_z":
        sort_by = asc(carts.c.total_price)
    else:
        sort_by = desc(carts.c.total_price)

    return run_query(select(carts).where(carts.c.status != "cart").limit(int(page)*int(page_size)).order_by(sort_by))
