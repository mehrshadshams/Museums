"""Gunicorn configuration."""
import multiprocessing

bind = '0.0.0.0:8080'

workers = 3
threads = 3
worker_class = 'gevent'

accesslog = '/app/logs/access.log'
errorlog = '/app/logs/error.log'
