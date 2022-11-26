from flask import Blueprint, request
from functions.products import valid_product, get_product_list, get_product_by_id
from functions.images import get_images_list, decode_image, get_image_by_images_url
from functions.categories import get_all_categories

products_bp = Blueprint("products", __name__, url_prefix="/products")
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@products_bp.route("", methods=["GET"])
def get_product():
    args = request.args
    sort_by = args.get("sort_by")
    category = args.get("category")
    product_name = args.get("product_name")
    condition = args.get("condition")
    page = args.get("page")
    page_size = args.get("page_size")
    price = args.get("price")

    if valid_product(category, product_name) == False:
        return {"message": "error, Item is not available"}, 400
    else:
        product = get_product_list(
            condition, product_name, category, price, page, page_size, sort_by)

        data = []
        for i in range(len(product)):
            image_list = get_images_list(product[0]["id"])
            dict = {
                "id": product[i]["id"],
                "title": product[i]["title"],
                "price": product[i]["price"],
                "image": image_list
            }

            data.append(dict)

        return {"data": data, "total_rows": len(product)}, 200


@ categories_bp.route("", methods=["GET"])
def get_category():
    categories = get_all_categories()
    data = []
    for i in range(len(categories)):
        dict = {
            "id": categories[i]["id"],
            "title": categories[i]["title"]
        }
        data.append(dict)

    return {"data": data}, 200


@ products_bp.route("/search_image", methods=["POST"])
def search_image():
    args = request.args
    image = args.get("image")

    image = decode_image(image)
    image = get_image_by_images_url(image)

    data = get_product_by_id(image[0]["product_id"])
    return {"category_id": f"{data[0]['category_id']}"}
