import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/mailapi'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    PASSWORD_PEPPER = 'krasserPfeffer'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True