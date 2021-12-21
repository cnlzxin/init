FROM python:3.6-alpine3.12 as builder

# eventlet
RUN apk add gcc
RUN apk add libc-dev

ENV USER=builder
RUN adduser -D -g '' ${USER}
USER ${USER}
WORKDIR /home/${USER}

RUN pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir eventlet==0.29.1 greenlet==0.4.17


FROM python:3.6-alpine3.12

ENV USER=python
RUN adduser -D -g '' ${USER}
USER ${USER}
WORKDIR /home/${USER}

RUN mkdir -p .local/lib/python3.6/site-packages
COPY --from=builder --chown=${USER}:${USER} /home/builder/.local/lib/python3.6/site-packages .local/lib/python3.6/site-packages

COPY --chown=${USER}:${USER} . .
RUN rm -rf docker

COPY --chown=${USER}:${USER} docker/requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r requirements.txt && rm requirements.txt

# gunicorn
ENV PATH="/home/${USER}/.local/bin:${PATH}"

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app", "-k", "eventlet", "--log-level", "debug"]
