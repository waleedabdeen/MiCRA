from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api import Classification, Requirements
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
# cors = CORS(app)
CORS(
    app,
    origins="http://localhost:3000",
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
logging.getLogger("flask_cors").level = logging.DEBUG
# app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.add_resource(Classification, "/classification")
api.add_resource(Requirements, "/requirements")


if __name__ == "__main__":
    app.run(debug=True)
