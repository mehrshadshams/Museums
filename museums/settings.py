import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SSL_DISABLE = False
    CELERY_BROKER_URL = "amqp://admin:mypass@rabbit:5672"    
    CELERY_RESULT_BACKEND = 'rpc://'

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}