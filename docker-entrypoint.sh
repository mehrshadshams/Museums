#! /usr/bin/env sh
set -e

exec "$@"

# exec gunicorn \
#     -b 0.0.0.0:8080 \
#     --access-logfile /app/logs/access.log \
#     --error-logfile /app/logs/error.log \
#     --threads 3 \
#     --workers 3 \
#     --worker-class gevent \
#     museums:app
