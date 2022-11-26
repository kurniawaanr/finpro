import secrets
import jwt

from sqlalchemy import Table, MetaData, insert, select, update, and_
from passlib.hash import sha256_crypt
from migrations.users import create_table_users
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_users()
users = Table("users", MetaData(bind=get_engine()), autoload=True)


def verify_user(email, password):
    user = run_query(select(users).where(users.c.email == email))

    if len(user) == 0:
        return False

    verify = sha256_crypt.verify(password, user[0]["password"])

    if verify == False:
        return False

    return user


def insert_user(values):
    return run_query(insert(users).values(values), commit=True)


def update_user_by_email(values, email):
    return run_query(update(users).where(users.c.email == email).values(values), commit=True)


def hash_password(password):
    return sha256_crypt.hash(password)


def gen_token(email, type):
    key = secrets.token_hex(16)
    return jwt.encode({"email": email, "type:": type}, key, "HS256")


def get_buyer_by_token(token):
    return run_query(select(users).where(and_(users.c.token == token, users.c.type == "buyer")))


def buyer_verification(token):
    buyer = get_buyer_by_token(token)

    if len(buyer) == 0:
        return False

    return True


def seller_verification(token):
    user = run_query(select(users).where(
        and_(users.c.token == token, users.c.type == "seller")))
    if len(user) == 0:
        return False

    return True


def update_user_by_token(values, token):
    return run_query(update(users).values(values).where(users.c.token == token), commit=True)


def update_seller_balance(revenue):
    seller = run_query(select(users).where(users.c.type == "seller"))
    return run_query(update(users).values({"balance": seller[0]["balance"] + revenue}).where(
        users.c.type == "seller"), commit=True)


def update_buyer_balance(token, amount):
    buyer = run_query(select(users).where(
        and_(users.c.type == "buyer", users.c.token == token)))
    return run_query(update(users).values({"balance": buyer[0]["balance"] + int(amount)}).where(and_(users.c.type == "buyer", users.c.token == token)), commit=True)


def get_seller_balance(token):
    user = run_query(select(users).where(
        and_(users.c.token == token, users.c.type == "seller")))
    return user[0]["balance"]
