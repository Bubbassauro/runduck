"""Initialize flask app"""
import os
from flask import Flask
from logging import Formatter
from flask.logging import default_handler

template_dir = os.path.abspath("build")
app = Flask(__name__, template_folder=template_dir, static_url_path="")
app.config.from_pyfile("../app.cfg")


class CustomFormatter(Formatter):
    # pass
    def format(self, record):
        CRED = "\33[31m"
        CEND = "\033[0m"
        if record.levelname == "ERROR":
            return f"{CRED}{super().format(record)}{CEND}"

        return super().format(record)


formatter = CustomFormatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
default_handler.setFormatter(formatter)

import runduck.routes
import runduck.api
