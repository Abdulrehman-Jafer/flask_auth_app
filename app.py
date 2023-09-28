from flask import Flask, request, jsonify, Response
from db import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    get_jwt_identity,
    jwt_required,
)

app = Flask(__name__)

SECRET_KEY = "MYBEAUTIFULSECRETKEY"
app.config["JWT_SECRET_KEY"] = SECRET_KEY

jwt = JWTManager().__init__(app)
bcrypt = Bcrypt(app)


# creating a auth route
@app.route("/signup", methods=["POST"])
def signup():
    user_name = request.json.get("user_name")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    if user_name is None or password is None or confirm_password is None:
        return jsonify(
            {
                "message": "please fill all the fields",
                "status": 400,
                "body": {
                    "user_name": user_name,
                    "password": password,
                    "confirm_password": confirm_password,
                },
            }
        )
    if password != confirm_password:
        return jsonify({"message": "passwords do not match"})
    try:
        encrypted_password = bcrypt.generate_password_hash(password=password).decode(
            "utf-8"
        )  # it was returning binary so decoded using utf-8
        inserted = db.users.insert_one(
            {"user_name": user_name, "password": encrypted_password}
        )
        if not inserted:
            return jsonify({"message": "User not created"})

        user_id_str = str(inserted.inserted_id)
        token = create_access_token(identity=user_id_str)
        return jsonify({"message": "Successfully created", "token": token}), 200
    except Exception as e:
        return str(e), 500


@app.route("/login", methods=["POST"])
def login():
    user_name = request.json.get("user_name")
    password = request.json.get("password")
    user = db.users.find_one({"user_name": user_name})
    if not user:
        return jsonify({"message": "user not found"})
    if not bcrypt.check_password_hash(user["password"], password=password):
        return jsonify({"message": "invalid credentials"})
    str_user_id = str(user["_id"])
    token = create_access_token(identity=str_user_id)
    return jsonify({"message": "login successful", "token": token})


# creating a CRUD app
@app.route("/<user_id>")
@jwt_required()
def index(user_id):
    try:
        user_id = get_jwt_identity()
        print(user_id)
        # todos =
        return db.todo.find({user_id: user_id}), 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True)
