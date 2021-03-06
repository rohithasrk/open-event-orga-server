"""Copyright 2015 Rafal Kowalski"""
import os

import sys
from flask import logging

from populate_db import populate
from app import current_app as app, celery
from app.models import db
from app.settings import set_settings

_basedir = os.path.abspath(os.path.dirname(__file__))


class Setup(object):

    @staticmethod
    def create_app():
        # app.config.from_object('config.TestingConfig')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG_TB_ENABLED'] = False
        app.config['CELERY_ALWAYS_EAGER'] = True
        app.config['CELERY_EAGER_PROPAGATES_EXCEPTIONS'] = True
        app.config['BROKER_BACKEND'] = 'memory'
        # app.config['CELERY_BROKER_URL'] = ''
        # app.config['CELERY_RESULT_BACKEND'] = ''
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'test.db')
        app.secret_key = 'super secret key'
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.ERROR)
        celery.conf.update(app.config)
        with app.test_request_context():
            db.create_all()
            populate()
            set_settings(secret='super secret key', app_name='Open Event')

        return app.test_client()

    @staticmethod
    def drop_db():
        with app.test_request_context():
            db.session.remove()
            db.drop_all()
