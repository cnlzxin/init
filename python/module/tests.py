import pytest
import requests
from locust import HttpUser, task

from utils.tools import extract_data_structure as extract
from .tasks import add, CALCULATE_QUEUE_NAME


def test_hello():
    assert 'hello' == 'hello'


def test_hello_with_local_service(client):
    """ 没有接口管理平台, 使用本地定义的数据进行测试 """
    rv = client.get('/api/hello')
    expect_rv_data = {'hello': 'world'}
    assert extract(expect_rv_data) == extract(rv.get_json())


def test_ipecho_with_remote_service(client):
    """ 有接口管理平台, 使用线上定义的数据进行测试 """
    rv = client.get('/api/ipecho')
    expect_rv_data = requests.get('https://ipecho.net/plain').text
    assert extract(expect_rv_data) == extract(rv.get_json())


@pytest.mark.celery(task_default_queue=CALCULATE_QUEUE_NAME)
def test_celery_tasks(celery_worker):
    assert add.delay(1, 2).get() == 3


class ModuleUser(HttpUser):

    @task
    def hello(self):
        self.client.get('/api/hello')
