"""API routes"""
import os
from flask import json
from flask import jsonify
from flask_restplus import Api
from flask_restplus import Resource
from runduck import app


api = Api(app, version='1.0', doc='/api/doc', prefix='/api', validate=False)
