import base64

from sqlalchemy import Table, MetaData, select, insert, delete
from migrations.images import create_table_images
from utils import run_query, get_engine
from sqlalchemy.exc import NoSuchTableError

create_table_images()
images = Table("images", MetaData(bind=get_engine()), autoload=True)


def get_images_list(product_id):
    image = run_query(select(images).where(
        images.c.product_id == product_id))

    image_list = []

    for i in range(len(image)):
        image_list.append(image[i]["images_url"])

    if len(image_list) <= 1:
        image_list = image_list[0]

    return image_list


def decode_image(image):
    base64_bytes = image.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)

    return sample_string_bytes.decode("ascii")


def get_image_by_images_url(image):
    return run_query(select(images).where(images.c.images_url == image))


def insert_images(images_list, product_id):
    for i in range(len(images_list)):
        run_query(insert(images).values(
            {"images_url": images_list[i], "product_id": product_id}), commit=True)


def delete_images(product_id):
    run_query(delete(images).where(
        images.c.product_id == product_id), commit=True)
