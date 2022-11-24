from flask import request
from endpoints.cart import user_bp, order_bp
from functions.users import get_buyer_by_token, update_buyer_balance
from functions.shipping_addresses import update_sa, get_address_by_token
from functions.carts import get_cart_by_token
from functions.products import get_product_by_id
from functions.sizes import get_size_by_size_id
from functions.images import get_images_list


@user_bp.route("", methods=["GET"])
def user_details():
    headers = request.headers
    Authentication = headers.get("Authentication")

    data = get_buyer_by_token(Authentication)

    return {
        "data":
            {
                "name": data[0]["name"],
                "email": data[0]["email"],
                "phone_number": data[0]["phone_number"]
            }
    }, 200


@user_bp.route("/shipping_address", methods=["POST"])
def change_sa():
    body = request.json
    headers = request.headers
    Authentication = headers.get("Authentication")

    update_sa(body, Authentication)
    user = get_buyer_by_token(Authentication)
    shipping_address = get_address_by_token(Authentication)

    return {
        "name": shipping_address[0]["name"],
        "phone_number": user[0]["phone_number"],
        "address": shipping_address[0]["address"],
        "city": shipping_address[0]["city"]
    }, 200


@ user_bp.route("/balance", methods=["POST"])
def top_up_balance():
    args = request.args
    headers = request.headers
    Authentication = headers.get("Authentication")
    amount = args.get("amount")

    update_buyer_balance(Authentication, amount)

    return {"message": "Top Up balance success"}, 200


@ user_bp.route("/balance", methods=["GET"])
def get_user_balance():
    headers = request.headers
    Authentication = headers.get("Authentication")

    data = get_buyer_by_token(Authentication)

    return {
        "data":
            {
                "balance": data[0]["balance"]
            }
    }, 200


@ order_bp.route("", methods=["GET"])
def user_orders():
    headers = request.headers
    Authentication = headers.get("Authentication")

    cart = get_cart_by_token("order", Authentication)
    shipping_address = get_address_by_token(Authentication)
    user = get_buyer_by_token(Authentication)

    data = []
    for i in range(len(cart)):
        size = get_size_by_size_id(cart[i]["size_id"])
        product = get_product_by_id(size[0]["product_id"])

        prods = []
        for x in range(len(product)):
            img = get_images_list(product[x]["id"])
            prod = {
                "id": product[x]["id"],
                "details": {
                    "quantity": cart[i]["quantity"],
                    "size": size[0]["size"],
                },
                "price": cart[i]["quantity"] * product[x]["price"],
                "image": img,
                "name": product[x]["title"]
            }
            prods.append(prod)

        dict = {
            "id": cart[i]["id"],
            "created_at": cart[i]["created_at"],
            "products": prods,
            "shipping_method": cart[i]["shipping_method"],
            "status": cart[i]["status"],
            "shipping_address": {
                "name": shipping_address[0]["name"],
                "phone_number": user[0]["phone_number"],
                "address": shipping_address[0]["address"],
                "city": shipping_address[0]["city"]
            }
        }

        data.append(dict)

    return {"data": data}, 200
