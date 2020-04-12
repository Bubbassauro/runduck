"""Runduck API"""
import os
from flask import render_template
from flask import send_from_directory
from runduck import app

build_path = os.path.abspath("build")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logo192.png")
def logo():
    return send_from_directory(build_path, "logo192.png")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(build_path, "favicon.ico")


@app.route("/manifest.json")
def manifest():
    print(build_path)
    return send_from_directory(build_path, "manifest.json")


@app.route("/static/<path:path>")
def serve_static(path):
    """Serve static files for the frontend"""
    static_path = f"{build_path}/static"
    return send_from_directory(static_path, path)

