from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api import Classification, Requirements, Artifacts
from classifier.configurations import read_env_vars
import logging

# env
conf = read_env_vars()

# logging
loggingLevel = logging.INFO if conf["server_env"] == "production" else logging.INFO
logging.basicConfig(level=loggingLevel)

# app
app = Flask(__name__)
CORS(
    app,
    origins="*",
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
logging.getLogger("flask_cors").level = logging.DEBUG

# api
api = Api(app)
api.add_resource(Classification, "/classification")
api.add_resource(Requirements, "/requirements")
api.add_resource(Artifacts, "/artifacts")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
