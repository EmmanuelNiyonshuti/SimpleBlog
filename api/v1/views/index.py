from flask import jsonify
from api.v1.views import app_views
from web_app.models import Post

@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"}), 200


@app_views.route("/all_post", strict_slashes=False)
def posts_num():
    posts = Post.query.all()
    return jsonify({"all_posts": len(posts)}), 200