FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev build-essential python3-dev libpython3-dev libssl-dev

WORKDIR /code-user-service

COPY . .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# CMD ["sh", "-c", "./migrate.sh && ./entrypoint.sh"]