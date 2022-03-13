FROM python:3.8.5

ENV USERNAME python
RUN mkdir /app

RUN useradd -ms /bin/bash ${USERNAME}
RUN chown ${USERNAME} /app
USER ${USERNAME}

WORKDIR /app
RUN pip install poetry==1.0.3
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./smarttesting /app/smarttesting
COPY ./tests /app/tests

STOPSIGNAL SIGINT
ENV FLASK_APP smarttesting.web_app:app
ENV APP_ENV=PROD
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
