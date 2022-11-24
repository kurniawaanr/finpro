import datetime
import traceback
import uuid
import base64
from passlib.hash import sha256_crypt
from functools import wraps
from sqlalchemy import Table, MetaData, select, insert, update
from utils import run_query, get_engine

##############################################################################################
# Helpers
##############################################################################################


def test(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
        print("-" * 100)
        print(f.__name__)
        print("-" * 100)
        global MAX_SCORE, FINAL_SCORE
        MAX_SCORE, FINAL_SCORE = 0, 0
        try:
            f(*args, **kwargs)
        finally:
            res = FINAL_SCORE, MAX_SCORE
            # reset final score before returning
            FINAL_SCORE = 0
            return res

    return dec


def assert_eq_dict(expression, expected: dict) -> bool:
    if not isinstance(expression, dict):
        return False

    for k in expected:
        if k not in expression:
            return False

    for k, v in expression.items():
        if k not in expected:
            return False
        if v != expected[k]:
            return False

    return True


def assert_eq(
    expression, expected, exc_type=AssertionError, hide: bool = False, err_msg=None
):
    try:
        if isinstance(expected, dict):
            if assert_eq_dict(expression, expected):
                return
        elif expression == expected:
            return

        errs = [err_msg] if err_msg else []
        if hide:
            expected = "<hidden>"
        err = "\n".join(
            [*errs, f"> Expected: {expected}", f"> Yours: {expression}"])
        raise exc_type(err)
    except Exception:
        raise


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
class COL:
    PASS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"


# special exception when something should've been printed, but wasn't
class DisplayError(Exception):
    pass


class Scorer:
    def __enter__(self):
        pass

    def __init__(self, score: float, desc: str):
        self.score = score
        global MAX_SCORE
        MAX_SCORE += score
        print(f"{COL.BOLD}{desc}{COL.ENDC} ({self.score} pts)")

    def __exit__(self, exc_type, exc_value, exc_tb):
        # add maximum score when passing these statements, otherwise 0
        if not exc_type:
            global FINAL_SCORE
            FINAL_SCORE += self.score
            print(COL.PASS, f"\tPASS: {self.score} pts", COL.ENDC)
        else:
            err_lines = [exc_type.__name__, *str(exc_value).split("\n")]
            errs = [
                "\t" + (" " * 4 if index else "") + line
                for index, line in enumerate(err_lines)
            ]
            print("{}{}".format(COL.WARNING, "\n".join(errs)))
            print(f"\t{COL.FAIL}FAIL: 0 pts", COL.ENDC)

        # skip throwing the exception
        return True


class safe_init:
    def __enter__(self):
        pass

    def __init__(self, max_score: int):
        self.max_score = max_score

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(traceback.format_exc())
            global MAX_SCORE
            MAX_SCORE = self.max_score
            return False

        return True


##############################################################################################
# Actual Tests
##############################################################################################


def assert_response(
    c,
    method: str,
    endpoint: str,
    json: dict = None,
    exp_json=None,
    exp_code: int = None,
    headers: dict = None,
):
    if not headers:
        headers = {}

    response = getattr(c, method)(endpoint, json=json, headers=headers)
    assert_eq(response.json, exp_json)
    assert_eq(response.status_code, exp_code)
    return response.json


class IsString:
    def __eq__(self, other):
        return isinstance(other, str)

    def __repr__(self):
        return "<must_be_a_string>"


def gen_uuid():
    # representative from each
    id = uuid.uuid4()
    return id


@test
def test_end_to_end():
    with safe_init(100):
        from app import app

        app.config.update({"TESTING": True})
        c = app.test_client()

##############################################################################################
# Example Data
##############################################################################################

    # tables
    banners = Table("banners", MetaData(bind=get_engine()), autoload=True)
    categories = Table("categories", MetaData(
        bind=get_engine()), autoload=True)
    users = Table("users", MetaData(bind=get_engine()), autoload=True)
    products = Table("products", MetaData(bind=get_engine()), autoload=True)
    images = Table("images", MetaData(bind=get_engine()), autoload=True)
    carts = Table("carts", MetaData(bind=get_engine()), autoload=True)
    sizes = Table("sizes", MetaData(bind=get_engine()), autoload=True)
    shipping_addresses = Table("shipping_addresses", MetaData(
        bind=get_engine()), autoload=True)

    # data
    banners_data = [
        {
            "id": f"{gen_uuid()}",
            "image": "/something/image.png",
            "title": "lorem ipsum blablabla"
        }
    ]

    categories_data = [
        {
            "id": f"{gen_uuid()}",
            "image": "/something/image.png",
            "title": "Category A"
        }
    ]

    seller_data = [
        {"id": f"{gen_uuid()}", "name": "Ilham Nur", "email": "ilham@gmail.com", "phone_number": "082713627",
         "password": f"{sha256_crypt.hash('password5679')}", "type": "seller", "balance": 0}
    ]

    products_data = [
        {
            "id": f"{gen_uuid()}",
            "title": "Item A",
            "price": 15000,
            "category_id": f"{categories_data[0]['id']}",
            "condition": "used",
            "product_detail": "lorem ipsum",
        },
        {
            "id": f"{gen_uuid()}",
            "title": "Nama product",
            "price": 1000,
            "category_id": f"{categories_data[0]['id']}",
            "condition": "used",
            "product_detail": "lorem ipsum",
        },
        {
            "id": f"{gen_uuid()}",
            "title": "Product a",
            "price": 10000,
            "category_id": f"{categories_data[0]['id']}",
            "condition": "used",
            "product_detail": "lorem ipsum",
        }
    ]

    sizes_data = [
        {
            "id": f"{gen_uuid()}",
            "product_id": products_data[1]["id"],
            "size": 'S'
        },
        {
            "id": f"{gen_uuid()}",
            "product_id": products_data[1]["id"],
            "size": 'M'
        },
        {
            "id": f"{gen_uuid()}",
            "product_id": products_data[1]["id"],
            "size": 'L'
        },
        {
            "id": f"{gen_uuid()}",
            "product_id": products_data[2]["id"],
            "size": 'M'
        },
    ]

    images_data = [
        {
            "product_id": products_data[0]["id"],
            "images_url": "/something/image.png"
        },
        {
            "product_id": products_data[1]["id"],
            "images_url": "/image/image1"
        },
        {
            "product_id": products_data[1]["id"],
            "images_url": "/image/image2"
        },
        {
            "product_id": products_data[2]["id"],
            "images_url": "/url/image.jpg"
        }
    ]

    # insert data
    run_query(insert(banners).values(banners_data), commit=True)
    run_query(insert(categories).values(categories_data), commit=True)
    run_query(insert(users).values(seller_data), commit=True)
    run_query(insert(products).values(products_data), commit=True)
    run_query(insert(images).values(images_data), commit=True)
    run_query(insert(sizes).values(sizes_data), commit=True)

    # variables
    image_name = "image_name.jpg"
    sample_string = categories_data[0]["image"]
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    buyer_token = []
    seller_token = []
    x = datetime.datetime.now()

##############################################################################################

    with Scorer(1, "Testing for Get Image"):
        assert_response(
            c,
            "get",
            f"/image/{image_name}",
            exp_code=200,
        )

    with Scorer(0.5, "Testing for Get Banner"):
        assert_response(
            c,
            "get",
            "/home/banner",
            exp_json={
                "data": [
                    {
                        "id": banners_data[0]["id"],
                        "image": "/something/image.png",
                        "title": "lorem ipsum blablabla"
                    }
                ]
            },
            exp_code=200,
        )

    with Scorer(0.5, "Testing for Get Category"):
        assert_response(
            c,
            "get",
            "/home/category",
            exp_json={
                "data": [
                    {
                        "id": categories_data[0]["id"],
                        "image": "/something/image.png",
                        "title": "Category A"
                    }
                ]
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for Sign-up"):
        assert_response(
            c,
            "post",
            "/sign-up",
            json={"name": "Raihan Parlaungan", "email": "raihan@gmail.com",
                  "phone_number": "081380737126", "password": "password1234"},
            exp_json={
                "message": "success, user created"},
            exp_code=201,
        )

        assert_response(
            c,
            "post",
            "/sign-up",
            json={"name": "Raymond Christhoper", "email": "raymond@gmail.com",
                  "phone_number": "082713626", "password": "password5678"},
            exp_json={
                "message": "success, user created"},
            exp_code=201,
        )

        assert_response(
            c,
            "post",
            "/sign-up",
            json={"name": "Raihan Parlaungan", "email": "raihan@gmail.com",
                  "phone_number": "081380737126", "password": "password1234"},
            exp_json={
                "message": "error, user already exists"},
            exp_code=409,
        )

    with Scorer(1, "Testing for Sign-in"):
        response = assert_response(
            c,
            "post",
            "/sign-in",
            json={"email": "raihan@gmail.com", "password": "password1233"},
            exp_json={"message": "error, Email or password is incorrect"},
            exp_code=401,
        )

        response = assert_response(
            c,
            "post",
            "/sign-in",
            json={"email": "raihan@gmail.com", "password": "password1234"},
            exp_json={
                "message": "Login success",
                "token": IsString(),
                "user_information":
                    {
                        "email": "raihan@gmail.com",
                        "name": "Raihan Parlaungan",
                        "phone_number": "081380737126",
                        "type": "buyer"
                }
            },
            exp_code=200,
        )
        buyer_token.append(response["token"])

        response = assert_response(
            c,
            "post",
            "/sign-in",
            json={"email": "raymond@gmail.com", "password": "password5678"},
            exp_json={
                "message": "Login success",
                "token": IsString(),
                "user_information":
                    {
                        "email": "raymond@gmail.com",
                        "name": "Raymond Christhoper",
                        "phone_number": "082713626",
                        "type": "buyer"
                }
            },
            exp_code=200,
        )
        buyer_token.append(response["token"])

        response = assert_response(
            c,
            "post",
            "/sign-in",
            json={"email": "ilham@gmail.com", "password": "password5679"},
            exp_json={
                "message": "Login success",
                "token": IsString(),
                "user_information":
                    {
                        "email": "ilham@gmail.com",
                        "name": "Ilham Nur",
                        "phone_number": "082713627",
                        "type": "seller"
                }
            },
            exp_code=200,
        )
        seller_token.append(response["token"])

    with Scorer(1, "Testing for Get Product List"):
        sort_bies = ["Price a_z", "Price z_a"]
        prices = [0, 10000]
        for sort_by in sort_bies:
            for price in prices:
                assert_response(
                    c,
                    "get",
                    "/products",
                    f"/products?page=1&page_size=100&sort_by={sort_by}&category=id category b&price={price}&condition=used&product_name=Item B",
                    exp_json={
                        "message": "error, Item is not available"},
                    exp_code=400,
                )

                assert_response(
                    c,
                    "get",
                    f"/products?page=1&page_size=100&sort_by={sort_by}&category=id category b&price={price}&condition=used&product_name=Item A",
                    exp_json={
                        "message": "error, Item is not available"},
                    exp_code=400,
                )

                assert_response(
                    c,
                    "get",
                    "/products",
                    f"/products?page=1&page_size=100&sort_by={sort_by}&category={products_data[0]['category_id']}&price={price}&condition=used&product_name=Item B",
                    exp_json={
                        "message": "error, Item is not available"},
                    exp_code=400,
                )

                assert_response(
                    c,
                    "get",
                    f"/products?page=1&page_size=100&sort_by={sort_by}&category={products_data[0]['category_id']}&price={price}&condition=used&product_name=Item A",
                    exp_json={
                        "data": [
                            {
                                "id": products_data[0]["id"],
                                "image": "/something/image.png",
                                "title": "Item A",
                                "price": 15000
                            }
                        ],
                        "total_rows": 1
                    },
                    exp_code=200,
                )

    with Scorer(0.5, "Testing for Get Category"):
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "data": [
                    {
                        "id": categories_data[0]["id"],
                        "title": "Category A"
                    }
                ]
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for Search Product by Image"):
        assert_response(
            c,
            "post",
            f"/products/search_image?image={base64_string}",
            exp_json={"category_id": products_data[1]["category_id"]},
            exp_code=200,
        )

    with Scorer(1, "Testing for Get Product Details"):
        assert_response(
            c,
            "get",
            f"/products/{products_data[1]['id']}",
            exp_json={
                "id": products_data[1]["id"],
                "images_url": ["/image/image1", "/image/image2"],
                "price": 1000,
                "product_detail": "lorem ipsum",
                "size": ["S", "M", "L"],
                "title": "Nama product",
            },
            exp_code=200,
        )

    carts_data = [
        {
            'id': f"{gen_uuid()}",
            "quantity": 9,
            "token": buyer_token[1],
            "size_id": sizes_data[3]["id"],
            "status": "cart"
        }
    ]

    run_query(insert(carts).values(carts_data), commit=True)

    with Scorer(2, "Testing for Add to Cart"):
        assert_response(
            c,
            "post",
            f"/cart",
            json={"id": sizes_data[3]["product_id"],
                  "quantity": 10, "size": "M"},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Unauthorized user"},
            exp_code=403,
        )

        assert_response(
            c,
            "post",
            f"/cart",
            json={"id": sizes_data[3]["product_id"],
                  "quantity": 10, "size": "M"},
            headers={"Authentication": buyer_token[1]},
            exp_json={"message": "Item added to cart"},
            exp_code=201,
        )

    run_query(update(carts).values({"quantity": 100}).where(
        carts.c.id == carts_data[0]["id"]), commit=True)

    with Scorer(0.5, "Testing for Get User's Carts"):
        assert_response(
            c,
            "get",
            "/cart",
            headers={"Authentication": buyer_token[1]},
            exp_json={
                "data": [
                    {
                        "id": f"{carts_data[0]['id']}",
                        "details": {
                            "quantity": 100,
                            "size": "M"
                        },
                        "price": 10000,
                        "image": "/url/image.jpg",
                        "name": "Product a"
                    }
                ],
                "total_rows": 1
            },
            exp_code=200,
        )

    shipping_addresses_data = [
        {
            "id": f"{gen_uuid()}",
            "name": "address name",
            "address": "22, ciracas, east jakarta",
            "city": "Jakarta",
            "token": buyer_token[1]
        }
    ]

    run_query(insert(shipping_addresses).values(
        shipping_addresses_data), commit=True)

    with Scorer(0.5, "Testing for Get User's Shipping Address"):
        assert_response(
            c,
            "get",
            "/user/shipping_address",
            headers={"Authentication": buyer_token[1]},
            exp_json={
                "data": {
                    "address": "22, ciracas, east jakarta",
                    "city": "Jakarta",
                    "id": IsString(),
                    "name": "address name",
                    "phone_number": "082713626",
                }
            },
            exp_code=200,
        )

    carts_data1 = [
        {
            'id': f"{gen_uuid()}",
            "quantity": 100,
            "token": buyer_token[1],
            "size_id": sizes_data[1]["id"],
            "status": "cart"
        }
    ]

    run_query(update(carts).values({"quantity": 20}).where(
        carts.c.id == carts_data[0]["id"]), commit=True)
    run_query(insert(carts).values(carts_data1), commit=True)

    with Scorer(2, "Testing for Get Shipping Price"):
        assert_response(
            c,
            "get",
            "/shipping_price",
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Unauthorized user"},
            exp_code=403,
        )

        assert_response(
            c,
            "get",
            "/shipping_price",
            headers={"Authentication": buyer_token[0]},
            exp_json={"message": "error, Cart is empty"},
            exp_code=400,
        )

        assert_response(
            c,
            "get",
            f"/shipping_price",
            headers={"Authentication": buyer_token[1]},
            exp_json={
                "data": [
                    {
                        "name": "regular",
                        "price": 55000
                    },
                    {
                        "name": "next day",
                        "price": 60000
                    }
                ]
            },
            exp_code=200,
        )

    with Scorer(1.5, "Testing for Create Order"):
        assert_response(
            c,
            "post",
            "/order",
            json={"shipping_method": "same day", "shipping_address":
                  {
                      "name": "address name",
                      "phone_number": "082713626",
                      "address": "22, ciracas, east jakarta",
                      "city": "Jakarta"
                  }
                  },
            headers={"Authentication": "12345678"},
            exp_json={"message": "error, Unauthorized user"},
            exp_code=403,
        )

        assert_response(
            c,
            "post",
            "/order",
            json={"shipping_method": "same day", "shipping_address":
                  {
                      "name": "address name",
                      "phone_number": "082713626",
                      "address": "22, ciracas, east jakarta",
                      "city": "Jakarta"
                  }
                  },
            headers={"Authentication": buyer_token[1]},
            exp_json={"message": "error, Please top up 355000"},
            exp_code=400,
        )

        assert_response(
            c,
            "post",
            "/user/balance?amount=355000",
            headers={"Authentication": buyer_token[1]},
            exp_json={"message": "Top Up balance success"},
            exp_code=200,
        )

        assert_response(
            c,
            "post",
            "/order",
            json={"shipping_method": "same day", "shipping_address":
                  {
                      "name": "address name",
                      "phone_number": "082713626",
                      "address": "22, ciracas, east jakarta",
                      "city": "Jakarta"
                  }
                  },
            headers={"Authentication": buyer_token[1]},
            exp_json={"message": "Order sucess"},
            exp_code=201,
        )

    with Scorer(1, "Testing for Delete Cart Item"):
        assert_response(
            c,
            "delete",
            f"/cart/{carts_data1[0]['id']}",
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Unauthorized user"},
            exp_code=403,
        )

        assert_response(
            c,
            "delete",
            f"/cart/{carts_data1[0]['id']}",
            headers={"Authentication": buyer_token[1]},
            exp_json={"message": "Cart deleted"},
            exp_code=200,
        )

    with Scorer(1, "Testing for User Details"):
        assert_response(
            c,
            "get",
            "/user",
            headers={"Authentication": buyer_token[0]},
            exp_json={
                "data":
                    {
                        "email": "raihan@gmail.com",
                        "name": "Raihan Parlaungan",
                        "phone_number": "081380737126"
                    }
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for Change Shipping Address"):
        assert_response(
            c,
            "post",
            "/user/shipping_address",
            headers={"Authentication": buyer_token[1]},
            json={
                "name": "address name",
                "address": "22, ciracas, east jakarta",
                "city": "Jakarta"
            },
            exp_json={
                "address": "22, ciracas, east jakarta",
                "city": "Jakarta",
                "name": "address name",
                "phone_number": "082713626"
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for Top-up Balance"):
        assert_response(
            c,
            "post",
            "/user/balance?amount=10000",
            headers={"Authentication": buyer_token[0]},
            exp_json={"message": "Top Up balance success"},
            exp_code=200,
        )

    with Scorer(1, "Testing for Get User Balance"):
        assert_response(
            c,
            "get",
            "/user/balance",
            headers={"Authentication": buyer_token[0]},
            exp_json={
                "data":
                    {
                        "balance": 10000
                    }
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for User Orders"):
        assert_response(
            c,
            "get",
            "/order",
            headers={"Authentication": buyer_token[1]},
            exp_json={
                "data": [
                    {
                        "id": carts_data[0]["id"],
                        "created_at": x.strftime("%a, %d %B %Y"),
                        "products": [
                            {
                                "id": products_data[2]["id"],
                                "details": {
                                    "quantity": 20,
                                    "size": "M"
                                },
                                "price": 200000,
                                "image": "/url/image.jpg",
                                "name": "Product a"
                            }
                        ],
                        "shipping_method": "same day",
                        "status": "waiting",
                        "shipping_address": {
                            "name": "address name",
                            "phone_number": "082713626",
                            "address": "22, ciracas, east jakarta",
                            "city": "Jakarta"
                        }
                    }
                ]
            },
            exp_code=200,
        )

    with Scorer(1, "Testing for Get Orders"):
        for sort_by in sort_bies:
            assert_response(
                c,
                "get",
                f"/orders?sort_by={sort_by}&page=1&page_size=25&is_admin=False",
                headers={"Authentication": buyer_token[0]},
                exp_json={"message": "error, user is not admin"},
                exp_code=400,
            )

            raymond = run_query(select(users).where(
                users.c.email == "raymond@gmail.com"))

            assert_response(
                c,
                "get",
                f"/orders?sort_by={sort_by}&page=1&page_size=25&is_admin=True",
                headers={"Authentication": seller_token[0]},
                exp_json={
                    "data": [
                        {
                            "id": carts_data[0]["id"],
                            "title": "Product a",
                            "size": "M",
                            "created_at": x.strftime("%a, %d %B %Y"),
                            "product_detail": "lorem ipsum",
                            "email": "raymond@gmail.com",
                            "images_url": "/url/image.jpg",
                            "user_id": raymond[0]["id"],
                            "total": 20
                        }
                    ]
                },
                exp_code=200,
            )

    with Scorer(2, "Testing for Create Product"):
        assert_response(
            c,
            "post",
            "/products",
            json={"product_name": "Product 1", "description": "Lorem ipsum", "images": [
                "image_1", "image_2", "image_3"], "condition": "new", "category": categories_data[0]["id"], "price": 10000},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Product added"},
            exp_code=201,
        )

    prod = run_query(select(products).where(products.c.title == "Product 1"))

    with Scorer(1, "Testing for Update Product"):
        assert_response(
            c,
            "put",
            "/products",
            json={"product_name": "Product 1", "description": "Lorem ipsum", "images": [
                "image_1", "image_2", "image_3"], "condition": "new", "category": categories_data[0]["id"], "price": 12000, "product_id": prod[0]["id"]},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Product is already exists"},
            exp_code=409,
        )

        assert_response(
            c,
            "put",
            "/products",
            json={"product_name": "Product 2", "description": "Lorem ipsum", "images": [
                "image_1", "image_2", "image_3"], "condition": "new", "category": categories_data[0]["id"], "price": 10000, "product_id": prod[0]["id"]},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Product updated"},
            exp_code=200,
        )

    with Scorer(1, "Testing for Delete Product"):
        assert_response(
            c,
            "delete",
            f"/products/{prod[0]['id']}",
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Product deleted"},
            exp_code=200,
        )

    with Scorer(1, "Testing for Create Category"):
        assert_response(
            c,
            "post",
            "/categories",
            json={"category_name": "Category B"},
            headers={"Authentication": buyer_token[0]},
            exp_json={'message': 'error, user is not admin'},
            exp_code=400,
        )

        assert_response(
            c,
            "post",
            "/categories",
            json={"category_name": "Category B"},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Category added"},
            exp_code=201,
        )

        assert_response(
            c,
            "post",
            "/categories",
            json={"category_name": "Category B"},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Category is already exists"},
            exp_code=409,
        )

    category = run_query(select(categories))

    with Scorer(1, "Testing for Update Category"):
        assert_response(
            c,
            "put",
            f"/categories/{category[1]['id']}",
            json={"category_name": "Category C",
                  "category_id": f"{category[1]['id']}"},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Category updated"},
            exp_code=200,
        )

        assert_response(
            c,
            "put",
            f"/categories/{category[0]['id']}",
            json={"category_name": "Category A",
                  "category_id": f"{category[0]['id']}"},
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, Category is already exists"},
            exp_code=409,
        )

    with Scorer(1, "Testing for Delete Category"):
        assert_response(
            c,
            "delete",
            f"/categories/{category[0]['id']}",
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "Category deleted"},
            exp_code=200,
        )

        assert_response(
            c,
            "delete",
            f"/categories/{category[0]['id']}",
            headers={"Authentication": seller_token[0]},
            exp_json={"message": "error, id is invalid"},
            exp_code=400,
        )

    with Scorer(1, "Testing for Get Total Sales"):
        assert_response(
            c,
            "get",
            "/sales",
            headers={"Authentication": seller_token[0]},
            exp_json={
                "data": {
                    "total": 300000
                }
            },
            exp_code=200,
        )


##############################################################################################


def highlight(s: str):
    print("=" * 100 + "\n")
    print(s)
    print("\n" + "=" * 100)


if __name__ == "__main__":
    highlight("Testing for Final Project...")
    tests = [test_end_to_end]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    highlight(
        f"{COL.BOLD}FINAL PROJECT PROGRESS:{COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC}"
    )
