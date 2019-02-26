FROM python:3.6

# RUN adduser --disabled-password --gecos '' webapp

RUN apt-get update && \
    apt-get --assume-yes upgrade && \
    apt-get --assume-yes install vim supervisor


COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.config.py /app/gunicorn.config.py

WORKDIR /app/

ADD requirements.txt /tmp/requirements.txt
ADD ./museums/ /app/museums/
ADD data.csv /app/museums/data.csv

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /app/logs

ENV FLASK_APP museums

# RUN chown -R webapp:webapp /app/

COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh

# USER webapp
VOLUME /app/logs

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["/usr/bin/supervisord"]