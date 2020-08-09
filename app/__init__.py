import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__,instance_relative_config=False)

    @app.route('/',methods=["GET"])
    def index():
        return "Testing volumes"

    return app