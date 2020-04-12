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
from runduck.jobinfo import get_job_details
from runduck.jobinfo import combine_data


cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
api = Api(app, version="1.0", doc="/api/doc", prefix="/api", validate=False)

parser = reqparse.RequestParser()
parser.add_argument(
    "force_refresh", location="args", default=False,
    type=inputs.boolean,
    help="Skip cache and force getting data from source")

@api.route("/jobs")
class Jobs(Resource):
    @api.expect(parser)
    def get(self):
        """
        List all jobs from all environments
        """
        args = parser.parse_args()
        force_refresh = args.get("force_refresh", False)
        interaction = DataInteraction()
        data = interaction.get_data("combined", force_refresh=force_refresh)
        return jsonify(data)

@api.route("/jobs/combine")
class JobsCombine(Resource):
    """Recombine all the data for the Jobs API from the raw data"""
    @api.expect(parser)
    def post(self):
        """Prepare all the data for the APIs
        This takes a few seconds if the raw data is already cached, it will
        take several minutes if the data is being refreshed from the source
        """
        args = parser.parse_args()
        force_refresh = args.get("force_refresh", False)
        combine_data(force_refresh=force_refresh)
        return jsonify({"message": "Data successfully combined"})

@api.route("/job/<string:env>/<string:jobid>")
class Job(Resource):
    """Get details of a job"""
    @api.expect(parser)
    def get(self, env, jobid):
        """
        Get details of one job in a specific environment
        """
        args = parser.parse_args()
        force_refresh = args.get("force_refresh", False)
        data = get_job_details(env=env, job_id=jobid, force_refresh=force_refresh)
        return jsonify(data)
