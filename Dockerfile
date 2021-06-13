FROM python:3.7-buster

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -q

RUN apt-get update && apt install apache2 libapache2-mod-wsgi-py3 python3-certbot-apache ./google-chrome*.deb -y

RUN rm google-chrome*.deb

COPY requirements.txt .env  /
COPY bin/* /usr/local/sbin/

RUN apache-setup.sh

RUN pip3 install -r requirements.txt
RUN python3 -m get_chromedriver
RUN mv chromedriver /usr/bin/


RUN a2ensite searchtube

CMD ["entrypiont.sh"]
