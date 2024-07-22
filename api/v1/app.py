from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, jsonify
from api.v1.views import app_views
from web_app import create_app, db


# app = Flask(__name__)
app = create_app()
# app.register_blueprint(app_views)

@app.errorhandler(NotFound)
def not_found_error(error):
    """
    Not found error
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(BadRequest)
def bad_request_error(error):
    return jsonify({"error": "Bad Request"}), 400

@app.teardown_appcontext
def teardown(exception):
    """
    This function is called when the app context tears down.
    It ensures the db session is closed after each request.
    """
    db.session.remove()



if __name__=="__main__":
    app.run(host='0.0.0.0', port=5001)
