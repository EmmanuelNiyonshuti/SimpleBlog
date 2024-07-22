from flask import jsonify, request, abort
from api.v1.views import app_views
from web_app import db, bcrypt
from web_app.models import User, Post
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@app_views.route("/users", methods=["GET", "POST"])
def get_users():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        users = User.query.paginate(page=page, per_page=per_page)
        if not users:
            abort(404)
        return jsonify({
                        "users": [user.to_dict() for user in users],
                        "meta": {
                            "page": users.page,
                            "per_page": users.per_page,
                            "total_pages": users.pages,
                            "total_items": users.total
                        }
                        }), 200

    elif request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400
        data = request.get_json()
        req_data = ["username", "email", "password"]
        if not all(field in data for field in req_data):
            return jsonify({"msg": "Missing required fields"}), 400
        try:
            if User.query.filter_by(username=data["username"]).first():
                return jsonify({"msg": "username is taken choose a different one"}), 400
            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"msg": "email is taken choose a different one"}), 400
            new_user = User(username=data["username"],
                        email=data["email"],
                        password=bcrypt.generate_password_hash(data["password"]))
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500

@app_views.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not all(field in data for field in ["email", "password"]):
        abort(400)
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    jwt_token = create_access_token(identity=user.id)
    return jsonify({
                "jwt_token": jwt_token,
                "user_id": user.id
                }), 200

@app_views.route("/users/<int:user_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@jwt_required()
def user(user_id):
    curr_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method in ["PUT", "PATCH"]:
        if curr_user_id != user_id:
            return jsonify({"error": "unauthorized access"}), 403
        if not request.is_json:
            abort(400)
        data = request.get_json()
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = bcrypt.generate_password_hash(data["password"])
        db.session.commit()
        return jsonify(user.to_dict()), 200
    elif request.method == "DELETE":
        if curr_user_id != user_id:
            return jsonify({"error": "unauthorized access"}), 403
        db.session.delete(user)
        db.session.commit()
        return jsonify({}), 200

@app_views.route("/users/<int:user_id>/posts", methods=["GET", "POST"])
@jwt_required()
def user_posts(user_id):
    user = User.query.get_or_404(user_id)
    curr_user_id = get_jwt_identity()
    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        posts = Post.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
        return jsonify({
                        "posts": [post.to_dict() for post in posts],
                        "meta": {
                            "page": posts.page,
                            "per_page": posts.per_page,
                            "total_pages": posts.pages,
                            "total_item": posts.total
                        }
                      }), 200
    elif request.method == 'POST':
        if curr_user_id != user_id:
            return jsonify({"error": "unauthorized access"}), 403
        if not request.is_json:
            abort(400)
        data = request.get_json()
        if not all(field in data for field in ["title", "content"]):
            return jsonify({"error": "Missing post title or contents"}), 400
        post = Post(title=data["title"], content=data["content"], user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_dict()), 201

