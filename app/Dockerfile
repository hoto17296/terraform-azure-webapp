FROM python:3.11

# Allow ssh access from Azure Portal
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd
COPY sshd_config /etc/ssh/

ENV POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH $POETRY_HOME/bin:$PATH
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY . .

RUN poetry install

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "main.py"]