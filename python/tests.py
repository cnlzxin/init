# locust patch
from gevent import monkey
monkey.patch_all()

import pytest

# rewrite assert statement, show more details on failure
for module in ['module.tests', 'utils.tests']:
    pytest.register_assert_rewrite(module)

from app import app
from config import CELERY_SETTINGS

from module.tests import *
from utils.tests import *

from module.tests import ModuleUser


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def celery_config():
    return CELERY_SETTINGS


class MixUser(ModuleUser):
    pass
