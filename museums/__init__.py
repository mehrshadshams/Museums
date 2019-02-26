import logging

from flask import Flask, Blueprint
from celery import Celery

from museums.settings import config, Config
from museums.api import api


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'], include=['museums.tasks'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)  # pylint: disable=invalid-name
app.config.update(
    CELERY_BROKER_URL=Config.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=Config.CELERY_RESULT_BACKEND
)
celery = make_celery(app)


def initialize_app(app):
    def _configure_app(app):
        app.config['SWAGGER_UI_DOC_EXPANSION'] = Config.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
        app.config['RESTPLUS_VALIDATE'] = Config.RESTPLUS_VALIDATE
        app.config['RESTPLUS_MASK_SWAGGER'] = Config.RESTPLUS_MASK_SWAGGER
        app.config['ERROR_404_HELP'] = Config.RESTPLUS_ERROR_404_HELP

    _configure_app(app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    app.register_blueprint(blueprint)

    import museums.controllers  # NOQA pylint: disable=wrong-import-position


LOGGER = logging.getLogger(__name__)
LOGGER.info('Starting app...')

initialize_app(app)
