from flask import (render_template, url_for, flash,
                    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from web_app import db
from web_app.models import Post, Comment
from web_app.posts.forms import PostForm, AddComment


posts= Blueprint("posts", __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>", strict_slashes=False)
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)



@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', "success")
        return redirect(url_for("posts.post", post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title=post.title, form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for("main.home"))

@posts.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = AddComment()
    if request.method == "POST":
        if form.validate_on_submit():
            comment = Comment(content=form.body.data, post_id=post.id, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash("successfully commented", "success")
            return redirect(url_for('posts.post', post_id=post.id))
    return render_template("add_comment.html", title=post.title, form=form, post=post)

@posts.route("/post/<int:post_id>/comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(post_id=None, comment_id=None):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(404)
    db.session.delete(comment)
    db.session.commit()
    flash("comment has been deleted", "success")
    return redirect(url_for("posts.post", post_id=post.id))
