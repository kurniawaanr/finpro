from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from functions.users import hash_password, insert_user, verify_user, gen_token, update_user_by_email
from utils import gen_id

signup_bp = Blueprint("signup", __name__, url_prefix="/sign-up")
signin_bp = Blueprint("signin", __name__, url_prefix="/sign-in")


@signup_bp.route("", methods=["POST"])
def sign_up():
    body = request.json
    password = body.get("password")

    try:
        body["type"] = "buyer"
        body["password"] = hash_password(password)
        body["balance"] = 0
        body["id"] = gen_id()
        insert_user(body)
        return {"message": "success, user created"}, 201

    except IntegrityError:
        return {"message": "error, user already exists"}, 409


@signin_bp.route("", methods=["POST"])
def sign_in():
    body = request.json
    email = body.get("email")
    password = body.get("password")

    user_information = verify_user(email, password)

    if user_information == False:
        return {"message": "error, Email or password is incorrect"}, 401

    else:
        body["token"] = gen_token(email, user_information[0]["type"])
        update_user_by_email(body, email)

        return {
            "user_information":
                {
                    "name": user_information[0]['name'],
                    "email": user_information[0]['email'],
                    "phone_number": user_information[0]['phone_number'],
                    "type": user_information[0]['type']
                },
            "token": body['token'],
            "message": "Login success"
        }, 200
