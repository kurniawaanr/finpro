from flask import Blueprint

from functions.banners import get_all_banners
from functions.categories import get_all_categories

home_bp = Blueprint("home", __name__, url_prefix="/home")


@home_bp.route("/banner", methods=["GET"])
def get_banner():
    return {"data": get_all_banners()}, 200


@home_bp.route("/category", methods=["GET"])
def get_category():
    return {"data": get_all_categories()}, 200
