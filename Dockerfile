FROM python:3.7-buster


RUN apt-get update && apt-get install -y \
    apt-utils \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3-certbot-apache

COPY requirements.txt .env  /
COPY bin/* /usr/local/sbin/


RUN pip3 install -r requirements.txt



CMD ["entrypiont.sh"]
