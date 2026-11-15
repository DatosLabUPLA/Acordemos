FROM python:3.5.10-slim-buster AS application

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir 'pip==20.3.4' \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

FROM application AS wsgi
RUN python -m pip install --no-cache-dir --only-binary=:all: gunicorn==20.1.0 \
    && mkdir -p /tmp/acordemos-build/media \
    && DJANGO_SECRET_KEY=collectstatic-build-only ACORDEMOS_DATA_DIR=/tmp/acordemos-build \
        python manage.py collectstatic --noinput \
    && rmdir /tmp/acordemos-build/media /tmp/acordemos-build
USER 10001:10001

FROM nginx:stable-alpine AS proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=wsgi /app/assets/ /srv/static/

FROM application AS development
