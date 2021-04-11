FROM python:3.9.4-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir -r /app/requirements.txt \
  && rm /app/requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings
EXPOSE 8000

# CMD gunicorn config.wsgi --workers 4 --bind 0.0.0.0:$PORT
CMD gunicorn config.wsgi --workers 4 --bind 0.0.0.0:8000
