FROM python:3.10.15-slim-bullseye as base

LABEL maintainer="apescara"

RUN apt-get update
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY /api/app.py .

ENV PORT 8080

CMD ["python", "app.py"]