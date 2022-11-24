from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request
from utils import gen_id
from endpoints.product_list import products_bp, categories_bp
from functions.users import seller_verification, get_buyer_by_token, get_seller_balance
from functions.carts import get_order_by_param
from functions.sizes import get_size_by_size_id, get_sizes_list
from functions.products import get_product_by_id, insert_product, duplicate_product, update_products, remove_product, delete_product_category
from functions.images import get_images_list, insert_images, delete_images
from functions.categories import duplicate_category, insert_category, update_category_by_id, category_exist, remove_category

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
sales_bp = Blueprint("sales", __name__, url_prefix="/sales")


@orders_bp.route("", methods=["GET"])
def get_orders():
    args = request.args
    headers = request.headers
    sort_by = args.get("sort_by")
    page = args.get("page")
    page_size = args.get("page_size")
    is_admin = args.get("is_admin", type=bool)
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False or is_admin != True:
        return {"message": "error, user is not admin"}, 400

    else:
        order = get_order_by_param(sort_by, page, page_size)
        data = []
        for i in range(len(order)):
            size = get_size_by_size_id(order[i]["size_id"])
            product = get_product_by_id(size[0]["product_id"])
            sz = get_sizes_list(product[0]["id"])
            img = get_images_list(product[0]["id"])
            buyer = get_buyer_by_token(order[i]["token"])

            dict = {
                "id": order[i]["id"],
                "title": product[0]["title"],
                "size": sz,
                "created_at": order[i]["created_at"],
                "product_detail": product[0]["product_detail"],
                "email": buyer[0]["email"],
                "images_url": img,
                "user_id": buyer[0]["id"],
                "total": order[i]["quantity"]
            }
            data.append(dict)

        return {"data": data}, 200


@products_bp.route("", methods=["POST"])
def create_product():
    body = request.json
    headers = request.headers
    product_name = body.get("product_name")
    description = body.get("description")
    images_list = body.get("images")
    condition = body.get("condition")
    category = body.get("category")
    price = body.get("price")
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400

    data = {"id": gen_id(), "title": product_name, "product_detail": description,
            "condition": condition, "category_id": category, "price": price}

    insert_product(data)
    insert_images(images_list, data["id"])

    return {"message": "Product added"}, 201


@products_bp.route("", methods=["PUT"])
def update_product():
    body = request.json
    headers = request.headers
    product_name = body.get("product_name")
    description = body.get("description")
    images_list = body.get("images")
    condition = body.get("condition")
    category = body.get("category")
    price = body.get("price")
    product_id = body.get("product_id")
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400
    elif duplicate_product(product_name, category, condition) == True:
        return {"message": "error, Product is already exists"}, 409
    else:
        data = {"title": product_name, "product_detail": description,
                "condition": condition, "category_id": category, "price": price}

        update_products(data, product_id)
        delete_images(product_id)
        insert_images(images_list, product_id)

        return {"message": "Product updated"}, 200


@products_bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    headers = request.headers
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400

    remove_product(product_id)
    delete_images(product_id)

    return {"message": "Product deleted"}, 200


@categories_bp.route("", methods=["POST"])
def create_category():
    headers = request.headers
    Authentication = headers.get("Authentication")
    body = request.json
    category_name = body.get("category_name")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400
    try:
        values = {"id": gen_id(), "title": category_name}
        insert_category(values)
        return {"message": "Category added"}, 201
    except IntegrityError:
        return {"message": "error, Category is already exists"}, 409


@categories_bp.route("/<category_id>", methods=["PUT"])
def update_category(category_id):
    headers = request.headers
    Authentication = headers.get("Authentication")
    body = request.json
    category_name = body.get("category_name")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400
    elif duplicate_category(category_name) == True:
        return {"message": "error, Category is already exists"}, 409
    else:
        values = {"title": category_name}
        update_category_by_id(values, category_id)
        return {"message": "Category updated"}, 200


@categories_bp.route("/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    headers = request.headers
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400
    elif category_exist(category_id) == False:
        return {"message": "error, id is invalid"}, 400
    else:
        delete_product_category(category_id)
        remove_category(category_id)
        return {"message": "Category deleted"}, 200


@sales_bp.route("", methods=["GET"])
def get_total_sales():
    headers = request.headers
    Authentication = headers.get("Authentication")

    if seller_verification(Authentication) == False:
        return {"message": "error, user is not admin"}, 400

    return {
        "data": {
            "total": get_seller_balance(Authentication)
        }
    }, 200
