from flaskblog import create_app, db
from flaskblog.models import User, Post
from flaskblog import admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskblog.models import AdminModelView

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin.add_view(AdminModelView(User, db.session))
        admin.add_view(AdminModelView(Post, db.session))
    app.run(debug=True)
