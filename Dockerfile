FROM python:3.11-slim-buster

ENV APP_HOME=/srv/mvp_crm/backend

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat \
    && pip install --upgrade pip \
    && mkdir -p $APP_HOME

WORKDIR $APP_HOME

COPY ./setup.py ./
RUN pip install -e ./
COPY . $APP_HOME

COPY ./start.sh ./
RUN chmod +x $APP_HOME/start.sh

ENTRYPOINT ["./start.sh"]