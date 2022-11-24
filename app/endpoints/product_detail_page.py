from flask import Blueprint, request
from utils import gen_id
from endpoints.product_list import products_bp
from functions.products import get_product_by_id
from functions.images import get_images_list
from functions.sizes import get_sizes_list, get_size_id
from functions.users import buyer_verification
from functions.carts import duplicate_product, insert_carts, update_quantity

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@products_bp.route("/<id>", methods=["GET"])
def get_product_details(id):
    product = get_product_by_id(id)
    image = get_images_list(id)
    size = get_sizes_list(id)

    return {
        "id": product[0]["id"],
        "title": product[0]["title"],
        "size": size,
        "product_detail": product[0]["product_detail"],
        "price": product[0]["price"],
        "images_url": image
    }, 200


@cart_bp.route("", methods=["POST"])
def add_to_cart():
    body = request.json
    headers = request.headers
    id = body.get("id")
    quantity = body.get("quantity")
    size = body.get("size")
    Authentication = headers.get("Authentication")

    size = get_size_id(id, size)

    if buyer_verification(Authentication) == False:
        return {"message": "error, Unauthorized user"}, 403
    elif duplicate_product(size, Authentication) == False:
        data = {"id": gen_id(), "quantity": quantity,
                "size_id": size, "status": "cart"}
        insert_carts(data)
    else:
        update_quantity(quantity, Authentication, size)
    return {"message": "Item added to cart"}, 201
