from flask import jsonify, request, abort 
from api.v1.views import app_views
from web_app.models import User, Post, Comment
from web_app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

@app_views.route("/posts")
def all_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    posts = Post.query.paginate(page=page, per_page=per_page)
    if not posts:
        abort(400)
    return jsonify({
                    "posts": [post.to_dict() for post in posts],
                    "meta": {
                        "page": posts.page,
                        "per_page": posts.per_page,
                        "total_page": posts.pages,
                        "total_items": posts.total
                        }
                    }), 200


@app_views.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

@app_views.route("/posts/<int:post_id>", methods=["PUT", "PATCH", "DELETE"])
@jwt_required()
def update_post(post_id):
    curr_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if request.method in ["PUT", "PATCH"]:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400
        data = request.get_json()
        if "title" in data:
            post.title = data["title"]
        if "content" in data:
            post.content = data["content"]
        db.session.commit()
        return jsonify(post.to_dict()), 200
    elif request.method == "DELETE":
        db.session.delete(post)
        db.session.commit()
        return jsonify({}), 200
    

@app_views.route("/posts/<int:post_id>/comments", methods=["GET", "POST"])
@jwt_required(optional=True)
def post_comments(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        abort(404)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    comments = Comment.query.filter_by(post_id=post_id).paginate(page=page, per_page=per_page)
    if not comments:
        abort(404)
    if request.method == "GET":
        return jsonify({
            "post_comments": [comment.to_dict() for comment in comments],
            "meta": {
                "page": comments.page,
                "per_page": comments.per_page,
                "total_pages": comments.pages,
                "total_items": comments.total
            }
        }), 200
    elif request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400
        data = request.get_json()
        if not "content" in data:
            return jsonify({"error": "Missing required field"}), 400
        user_id = get_jwt_identity()
        comment = Comment(content=data["content"], post_id=post_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return jsonify(comment.to_dict()), 201


@app_views.route("/posts/<int:post_id>/comments/<int:comment_id>")
def get_comment(post_id, comment_id):
    comment = Comment.filter_by(id=comment_id, post_id=post_id).first()
    if not comment:
        abort(400)
    return jsonify(comment.to_dict())

@app_views.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(post_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
    if not comment:
        abort(400)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({}), 200


            
