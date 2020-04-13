"""Initialize flask app"""
import os
from flask import Flask

template_dir = os.path.abspath("build")
app = Flask(__name__, template_folder=template_dir, static_url_path="")
app.config.from_pyfile("../app.cfg")

import runduck.routes
import runduck.api
