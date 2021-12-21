from celery import Celery


def extract_data_structure(data):
    """ 提取数据结构, 用于接口测试 """

    if isinstance(data, dict):
        return {key: (type(value) if not isinstance(value, (dict, list))
                      else extract_data_structure(value))
                for key, value in data.items()}

    if isinstance(data, list):
        return [extract_data_structure(data[0])] if data else type(data)

    return type(data)


def make_celery(name, settings, context):
    """ 创建 celery 的实例 """
    celery = Celery(name)
    celery.conf.update(settings)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
