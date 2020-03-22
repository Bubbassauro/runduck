"""Runduck API"""
import os
from flask import render_template
from flask import send_from_directory
from runduck import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def manifest():
    static_path = os.path.abspath("../runduck-ui/build")
    return send_from_directory(static_path, "manifest.json")


@app.route("/static/<path:path>")
def serve_static(path):
    """Serve static files for the frontend"""
    print(path)
    static_path = os.path.abspath("../runduck-ui/build/static")

    return send_from_directory(static_path, path)

