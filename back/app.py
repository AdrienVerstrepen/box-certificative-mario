import psycopg2
import os
import flask
from routes.user import userBlueprint

app = flask.Flask(__name__)

app.register_blueprint(userBlueprint)

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')

@app.route("/")
def index():
    return "Homepage of GeeksForGeeks"

import routes.user

if __name__ == '__main__':
    app.run(debug=True, port=8000)
