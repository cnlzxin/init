import os
from urllib.parse import quote

PROJECT_NAME = 'project'
DATABASE_NAME = 'project'

VERSION = os.getenv('VERSION') or 'alpha'

# Server
DEBUG = (os.getenv('DEBUG') == 'True')
SECRET_KEY = (b'\xaa\xc5\xc6\xcc\x87\xc59\x0e\x0eN\xcbfh'
              b'\x14\xf4#j\x82\x9d\x8boD\xce\xb9')

# MongoDB
MONGODB_SETTINGS = {
    'host': os.getenv('MONGODB_HOST', 'mongo'),
    'port': int(os.getenv('MONGODB_PORT', 27017)),
    'db': os.getenv('MONGODB_DB_NAME', DATABASE_NAME)
}

# RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWD = quote(os.getenv('RABBITMQ_PASSWD', 'guest'))      # 可以包含特殊字符
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', PROJECT_NAME)

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWD = quote(os.getenv('REDIS_PASSWD', 'redis'))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Celery
CELERY_SETTINGS = {
    'broker_url': (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWD}@'
                   f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'),
    'result_backend': (f'redis://:{REDIS_PASSWD}@{REDIS_HOST}:{REDIS_PORT}'
                       f'/{REDIS_DB}'),
    'task_queue_max_priority': 10,      # 最大优先级
    'task_default_priority': 5,         # 默认优先级
    'timezone': 'UTC',                  # 统一时间标准
    'imports': ['tasks'],
}
