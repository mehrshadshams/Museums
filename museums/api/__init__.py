import logging
from flask_restplus import Api

from .tasks import api as ns1

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

api = Api(
    title='Museums',
    version='1.0',
    description='A description'
)

api.add_namespace(ns1)


@api.errorhandler
def default_error_handler(e):  # NOQA pylint: disable=unused-argument
    message = 'An unhandled exception occurred.'
    log.exception(message)
    log.warning(message)
    print(e)

    return {'message': message}, 500
