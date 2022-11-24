from flask import Flask, send_file

from migrations.banners import create_table_banners
from migrations.carts import create_table_carts
from migrations.categories import create_table_categories
from migrations.images import create_table_images
from migrations.products import create_table_products
from migrations.shipping_addresses import create_table_shipping_addresses
from migrations.sizes import create_table_sizes
from migrations.users import create_table_users

from endpoints.home import home_bp
from endpoints.authentication import signup_bp, signin_bp
from endpoints.product_list import products_bp, categories_bp
from endpoints.product_detail_page import cart_bp, products_bp
from endpoints.cart import user_bp, shipping_price_bp, order_bp, cart_bp
from endpoints.profile_page import user_bp, order_bp
from endpoints.admin_page import orders_bp, sales_bp, products_bp, categories_bp


def create_app():
    app = Flask(__name__)

    blueprints = [orders_bp, sales_bp, signup_bp, signin_bp, user_bp, shipping_price_bp,
                  order_bp, home_bp, cart_bp, products_bp, categories_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.route("/image/<image_name>", methods=["GET"])
    def get_image(image_name):
        extension = image_name.split(".")
        extension = extension[len(extension)-1]
        return send_file('images/'+image_name, mimetype=f"image/{extension}"), 200

    @app.errorhandler(Exception)
    def handle_error(e: Exception):
        return (({"message": "error, " + str(e)}), 404)

    return app


app = create_app()

# Uncomment this before deploy
app.run(debug=True)
