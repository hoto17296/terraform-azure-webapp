FROM python:3.11

ENV POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH $POETRY_HOME/bin:$PATH
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY . .

RUN poetry install

CMD ["python", "main.py"]