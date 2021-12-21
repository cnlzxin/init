# 简介

Python 初始化时的项目, 包含单元测试、代码覆盖率检查、压力测试、性能分析、消息队列、镜像构建

单元测试:

```
$ pytest tests.py -v
tests.py::test_hello PASSED                                             [ 20%]
tests.py::test_hello_with_local_service PASSED                          [ 40%]
tests.py::test_ipecho_with_remote_service PASSED                        [ 60%]
tests.py::test_celery_tasks PASSED                                      [ 80%]
tests.py::test_extract_data_structure_tools PASSED                      [100%]
```

代码覆盖率检查:

```
$ coverage run --source . --concurrency gevent -m pytest tests.py -v
$ coverage report
Name                 Stmts   Miss  Cover
----------------------------------------
app.py                  12      1    92%
config.py               18      0   100%
module/__init__.py       1      0   100%
module/models.py         0      0   100%
module/tasks.py          7      0   100%
module/tests.py         20      1    95%
module/views.py          6      0   100%
tasks.py                 1      0   100%
tests.py                18      0   100%
utils/__init__.py        0      0   100%
utils/tests.py          14      0   100%
utils/tools.py          16      2    88%
----------------------------------------
TOTAL                  113      4    96%
```

性能分析:
```
$ pytest tests.py -v --profile

         105421 function calls (102112 primitive calls) in 3.207 seconds

   Ordered by: cumulative time
   List reduced from 2942 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    15/13    0.000    0.000    2.399    0.185 runner.py:213(call_and_report)
   105/48    0.001    0.000    2.399    0.050 hooks.py:272(__call__)
    15/13    0.000    0.000    2.396    0.184 runner.py:241(call_runtest_hook)
    15/13    0.000    0.000    2.396    0.184 runner.py:299(from_call)
    15/13    0.000    0.000    2.396    0.184 runner.py:256(<lambda>)
   105/48    0.000    0.000    2.333    0.049 manager.py:90(_hookexec)
   105/48    0.000    0.000    2.333    0.049 manager.py:84(<lambda>)
   105/48    0.001    0.000    2.332    0.049 callers.py:157(_multicall)
    93/26    2.287    0.025    2.288    0.088 hub.py:126(sleep)
      5/4    0.000    0.000    2.222    0.555 runner.py:107(pytest_runtest_protocol)
      5/4    0.000    0.000    2.221    0.555 runner.py:115(runtestprotocol)
        5    0.000    0.000    2.207    0.441 runner.py:174(pytest_runtest_teardown)
  418/166    0.000    0.000    2.059    0.012 {built-in method builtins.next}
        5    0.000    0.000    2.045    0.409 runner.py:416(teardown_exact)
        5    0.000    0.000    2.044    0.409 runner.py:420(_teardown_towards)
        7    0.000    0.000    2.044    0.292 runner.py:384(_pop_and_teardown)
        7    0.000    0.000    2.044    0.292 runner.py:403(_teardown_with_finalization)
        7    0.000    0.000    2.044    0.292 runner.py:388(_callfinalizers)
    19/11    0.000    0.000    2.044    0.186 fixtures.py:1019(finish)
        4    0.000    0.000    2.044    0.511 fixtures.py:934(_teardown_yield_fixture)
```


# 运行环境

Python 3.6
Flask 1.1
MongoDB 3.6

CentOS 7
Docker 19.03

Alpine 3.12                     # Docker 基础镜像环境

RabbitMQ 3.7
Redis 3.2.10


# 配置开发环境

安装依赖, 在国内使用阿里云的镜像, 要快一些:

    pip install -i https://mirrors.aliyun.com/pypi/simple -r docker/requirements.txt
    pip install -i https://mirrors.aliyun.com/pypi/simple -r docker/requirements-dev.txt

启动数据库服务:

    docker-compose -f docker/database.yml up -d

通过 https://localhost:15672 访问 RabbitMQ 的 Web 管理页面, 添加 `virtual host`

添加数据库主机名映射:

    echo '127.0.0.1    mongo rabbitmq redis' >> /etc/hosts


# 开发流程

没有接口管理平台:

1. docs/api.md 添加接口说明
2. module/tests.py 添加接口样例数据, 并添加单元测试样例
3. module/views.py 添加业务逻辑

有接口管理平台:

1. 线上定义接口及返回的样例数据
2. module/tests.py 添加单元测试样例
3. module/views.py 添加业务逻辑

运行项目:

    export DEBUG=True && python app.py

生产环境中运行的命令 (调试模式):

    gunicorn -w 4 -b 127.0.0.1:8000 -k eventlet app:app --log-level debug --reload

单元测试:

    export PYTHONWARNINGS="ignore:Unverified HTTPS request,ignore:Unknown pytest.mark.celery"
    pytest tests.py -v

代码覆盖率检查:

    coverage run --source . --concurrency gevent -m pytest tests.py -v
    coverage report
    coverage html               # 生成 htmlcov, 浏览器打开 htmlcov/index.html, 可查看详情

压力测试 (http://localhost:8089):

    locust -f tests.py -l       # 查看 HttpUser 列表
    locust -f tests.py --web-host localhost MixUser

性能分析:

    pytest tests.py -v --profile
    python -m pstats prof/combined.prof

单元测试、代码覆盖率检查、性能分析可以一起运行:

    coverage run --source . --concurrency gevent -m pytest tests.py -v --profile
    coverage report
    python -m pstats prof/combined.prof

更新版本号:

    修改 .env 文件中的 VERSION 值

说明:

- export 相关的命令可以放到 shell 的配置文件中, 比如: `echo 'export DEBUT=True' >> .zshrc`, 然后 `source` 一下


# 生产环境部署

查看配置:

    docker-compose -f docker/project.yml --env-file .env config

构建镜像:

    docker-compose -f docker/project.yml --env-file .env build

部署:

    docker-compose -f docker/database.yml --env-file .env up -d
    docker-compose -f docker/project.yml --env-file .env up -d

查看日志:

    docker logs -f --tail 10 project
    docker logs -f --tail 10 beat
    docker logs -f --tail 10 worker


# 注意事项

配置: 修改 config.py 文件中的 SECRET_KEY:

    >>> import os
    >>> os.urandom(24)
    b'\xaa\xc5\xc6\xcc\x87\xc59\x0e\x0eN\xcbfh\x14\xf4#j\x82\x9d\x8boD\xce\xb9'

配置: 修改 config.py 文件中的 PROJECT_NAME 和 DATABASE_NAME:

    PROJECT_NAME = 'project'
    DATABASE_NAME = 'project'

项目重命名: 将 docker 目录下的 project.yml 文件重命名:

    project.yml -> your_project_name.yml

模块重命名: module 模块是个样例, 需要改成你自己模块的名字, 另外还涉及到一些引用, 其中的模块名也需要改一下:

    module -> your_module_name
    tasks.py
    tests.py

删减: 使用时还需要根据实际情况做些删减工作, 比如: 如果用不到消息队列, 那么相关的配置、代码都是可以清理掉的:

    database.yml
    tasks.py
    tests.py
    config.py

部署:

- 生产环境中, 如果数据库、消息队列等服务采集分布式部署, 最好为不同的项目添加独立的账号, 并且使用证书对通信过程进行加密
- 生产环境中, 单机部署时, 如果需要将容器的端口映射到宿主机, 尽量使用 `127.0.0.1:27017:27017` 的形式, 不要使用 `0.0.0.0:27017:27017`, 会有些安全方面的问题


# 其他

压力测试: 要对多个模块进行压力测试时, 编写 tests.py:

    class MixUser(ModuleAUser, ModuleBUser):
        pass

locust web 页面中可配置的参数:

1. total users: 要模拟的用户数量
2. spawn rate: 用户增长速度/秒
3. host: 本地起的服务, 也可以是线上的, 前面需要带有 `http://`

示例: 配置 (10, 1, http://localhost:8000) 代表用户每秒会增长一个, 10 秒后会达到最大值, 然后以 10 个用户的并发量对 http://localhost:8000 上运行的接口进行压力测试
