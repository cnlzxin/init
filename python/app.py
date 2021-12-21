from flask import Flask
from flask_mongoengine import MongoEngine

import module
from config import PROJECT_NAME
from utils.tools import make_celery

# init app
app = Flask(PROJECT_NAME)
app.config.from_object('config')

# connect to the database
MongoEngine(app)

# register route
app.register_blueprint(module.bp)

# init celery instance
celery = make_celery(app.import_name, app.config['CELERY_SETTINGS'],
                     app.app_context)


if __name__ == '__main__':
    app.run('localhost', 8000)
