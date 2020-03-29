"""API routes"""
import os
from flask import json
from flask import jsonify
from flask_cors import CORS
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_restplus import inputs
from runduck import app
from runduck.datainteraction import DataSource
from runduck.datainteraction import DataInteraction
from runduck.jobinfo import read_environment


cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
api = Api(app, version="1.0", doc="/api/doc", prefix="/api", validate=False)

parser = reqparse.RequestParser()
parser.add_argument(
    "force_refresh", location="args", default=False,
    type=inputs.boolean,
    help="Skip cache and force getting data from source")

@api.route("/jobs")
class Projects(Resource):

    @api.expect(parser)
    def get(self):
        interaction = DataInteraction(env="all")
        data = interaction.get_data("projects")
        return jsonify(data)
