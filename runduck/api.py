"""API routes"""
import os
from flask import json
from flask import jsonify
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_restplus import inputs
from runduck import app
from runduck.datainteraction import DataSource
from runduck.jobinfo import read_all_data


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
        args = parser.parse_args()
        data = read_all_data(live_data_source=DataSource.API, force_refresh=args.get("force_refresh"))
        return jsonify(data)
