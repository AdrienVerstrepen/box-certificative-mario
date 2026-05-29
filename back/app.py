import psycopg2
import os
import flask
from routes.places import placesBlueprint
from routes.tour import tourBlueprint
from routes.user import userBlueprint

app = flask.Flask(__name__)

allowed_origins = {
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost,http://localhost:80,http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
}


@app.after_request
def add_cors_headers(response):
    """
    Add CORS headers for browser requests from the front-end dev and Docker origins.
    """
    origin = flask.request.headers.get("Origin")
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    return response


app.register_blueprint(tourBlueprint, url_prefix="/api")
app.register_blueprint(placesBlueprint, url_prefix="/api")
app.register_blueprint(userBlueprint, url_prefix="/api")

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')

import routes.user

if __name__ == '__main__':
    app.run(debug=True, port=8000)
