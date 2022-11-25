import os
import uuid
import datetime
from sqlalchemy import create_engine, text


def get_engine():

    # UNCOMMENT THIS BEFORE DEPLOY
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        "users",
        "password",
        "34.143.213.160",
        5432,
        "fashion-campus-db",
    )

    return create_engine(engine_uri, future=True)

    # COMMENT THIS BEFORE DEPLOY
    # return create_engine("sqlite:///fashion-campus.db", future=True)


def run_query(query, commit: bool = False):
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]


def gen_id():
    return str(uuid.uuid4())


def created_at():
    x = datetime.datetime.now()
    return x.strftime("%a, %d %B %Y")
