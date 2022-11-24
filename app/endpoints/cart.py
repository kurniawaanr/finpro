from flask import Blueprint, request
from utils import created_at, gen_id
from endpoints.product_detail_page import cart_bp
from functions.carts import get_cart_by_token, empty_cart, get_ship_price, update_carts, delete_cart
from functions.sizes import get_size_by_size_id
from functions.products import get_product_by_id
from functions.images import get_images_list
from functions.users import get_buyer_by_token, buyer_verification, update_user_by_token, update_seller_balance
from functions.shipping_addresses import get_address_by_token, shipp_ad_exist, insert_sa, update_sa

user_bp = Blueprint("user", __name__, url_prefix="/user")
shipping_price_bp = Blueprint(
    "shipping_price", __name__, url_prefix="/shipping_price")
order_bp = Blueprint("order", __name__, url_prefix="/order")


@cart_bp.route("", methods=["GET"])
def get_user_cart():
    headers = request.headers
    Authentication = headers.get("Authentication")

    cart = get_cart_by_token("cart", Authentication)

    data = []
    for i in range(len(cart)):
        size = get_size_by_size_id(cart[i]["size_id"])
        product = get_product_by_id(size[0]["product_id"])
        dict = {
            "id": cart[i]["id"],
            "details": {
                "quantity": cart[i]["quantity"],
                "size": size[0]["size"]
            },
            "price": product[0]["price"],
            "image": get_images_list(size[0]["product_id"]),
            "name": product[0]["title"]
        }

        data.append(dict)

    return {
        "data": data,
        "total_rows": len(data)
    }, 200


@ user_bp.route("/shipping_address", methods=["GET"])
def get_user_sa():
    headers = request.headers
    Authentication = headers.get("Authentication")

    user = get_buyer_by_token(Authentication)
    shipping_address = get_address_by_token(Authentication)

    return {
        "data":
            {
                "id": shipping_address[0]["id"],
                "name": shipping_address[0]["name"],
                "phone_number": user[0]["phone_number"],
                "address": shipping_address[0]["address"],
                "city": shipping_address[0]["city"]
            }
    }, 200


@ shipping_price_bp.route("", methods=["GET"])
def get_shipping_price():
    headers = request.headers
    Authentication = headers.get("Authentication")

    if buyer_verification(Authentication) == False:
        return {"message": "error, Unauthorized user"}, 403
    elif empty_cart(Authentication) == True:
        return {"message": "error, Cart is empty"}, 400
    else:
        cart = get_cart_by_token("cart", Authentication)

        regular_price = 0
        next_day_price = 0
        for i in range(len(cart)):
            size = get_size_by_size_id(cart[i]["size_id"])
            product = get_product_by_id(size[0]["product_id"])

            price = cart[i]["quantity"] * product[0]["price"]

            regular_price += get_ship_price(
                shipping_method="regular", total_price=price)
            next_day_price += get_ship_price(
                shipping_method="next day", total_price=price)

        return {
            "data":
                [
                    {
                        "name": "regular",
                        "price": regular_price
                    },
                    {
                        "name": "next day",
                        "price": next_day_price
                    }
                ]
        }, 200


@ order_bp.route("", methods=["POST"])
def create_order():
    body = request.json
    headers = request.headers
    shipping_method = body.get("shipping_method")
    shipping_address = body.get("shipping_address")
    name = shipping_address.get("name")
    phone_number = shipping_address.get("phone_number")
    address = shipping_address.get("address")
    city = shipping_address.get("city")
    Authentication = headers.get("Authentication")

    if buyer_verification(Authentication) == False:
        return {"message": "error, Unauthorized user"}, 403

    cart = get_cart_by_token("cart", Authentication)
    user = get_buyer_by_token(Authentication)

    total_price = 0
    for i in range(len(cart)):
        size = get_size_by_size_id(cart[i]["size_id"])
        product = get_product_by_id(size[0]["product_id"])
        price = cart[i]["quantity"] * product[0]["price"]
        total_price += price + get_ship_price(shipping_method, price)

    diff = total_price - user[0]["balance"]

    if diff > 0:
        return {"message": f"error, Please top up {diff}"}, 400
    else:
        update_user_by_token(
            {"balance": abs(diff), "phone_number": phone_number}, Authentication)
        for i in range(len(cart)):
            size = get_size_by_size_id(cart[i]["size_id"])
            product = get_product_by_id(size[0]["product_id"])

            price = cart[i]["quantity"] * product[0]["price"]
            total_price = price + get_ship_price(shipping_method, price)
            update_seller_balance(price)
            update_carts({"shipping_method": shipping_method, "status": "waiting",
                          "created_at": created_at(), "total_price": total_price}, cart[i]["id"])

        if shipp_ad_exist == False:
            insert_sa({"id": gen_id(), "name": name, "address": address,
                      "city": city, "token": Authentication})
        else:
            update_sa({"name": name, "address": address,
                      "city": city}, Authentication)

        return {"message": "Order sucess"}, 201


@ cart_bp.route("/<cart_id>", methods=["DELETE"])
def delete_cart_item(cart_id):
    headers = request.headers
    Authentication = headers.get("Authentication")

    if buyer_verification(Authentication) == False:
        return {"message": "error, Unauthorized user"}, 403
    else:
        delete_cart(cart_id)
        return {"message": "Cart deleted"}, 200
