import logging
import requests

from flask import jsonify, abort, Response
from flask_restplus import Namespace, Resource, reqparse

# from museums.tasks import longtime_add

api = Namespace('Tasks', description='Start Tasks')

log = logging.getLogger(__name__)

# Define URL requirement
url_upload_parser = reqparse.RequestParser()
url_upload_parser.add_argument('url', location='args', required=True)


@api.route('/')
class TaskExecutor(Resource):
    @api.doc('Execute Task')
    def post(self):        
        from museums.data import extract_list_of_museum_data

        extract_list_of_museum_data()

        return "started"
