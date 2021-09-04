FROM python:3.8.3-slim
USER root

RUN set -x \
    && apt-get -y update \
    && apt-get install -y vim cron nginx supervisor

COPY server/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

#nginx
COPY nginx.conf /etc/nginx/sites-available/
RUN set -x \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf \
    && echo "daemon off;" | tee -a /etc/nginx/nginx.conf

# Copy supervisor.conf
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Add bootstrap script and make it executable
COPY bootstrap.sh /root/bootstrap.sh
RUN chown root:root /root/bootstrap.sh && chmod a+x /root/bootstrap.sh

# Copy server source code to python path
COPY server /root/server
WORKDIR /root/server
ENV TZ=Asia/Taipei

ENTRYPOINT ["/root/bootstrap.sh"]
