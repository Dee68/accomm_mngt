FROM docker.io/python:3.12.2 as python

# Stage 1: Build wheels
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements /usr/src/app/requirements

RUN pip wheel --wheel-dir /usr/src/app/wheels -r /usr/src/app/requirements/local.txt

# Stage 2: Application runtime
FROM python as python-run-stage

ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    sudo git bash-completion nano ssh \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles

COPY --from=python-build-stage /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && \
    rm -rf /wheels/

COPY ./docker/local/django/entrypoint.sh /entrypoint
COPY ./docker/local/django/start.sh /start

RUN chmod +x /entrypoint /start

RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT [ "/entrypoint" ]
CMD [ "/start" ]
