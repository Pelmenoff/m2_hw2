FROM python:latest

ENV APP_HOME /app

WORKDIR $APP_HOME

RUN pip install poetry

COPY dedalus/ $APP_HOME/

RUN poetry install

EXPOSE 8888

ENTRYPOINT ["poetry", "run", "python", "-m", "dedalus.bot"]