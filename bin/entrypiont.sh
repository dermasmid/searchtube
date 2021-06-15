#!/bin/bash


if [ ! -f  /etc/apache2/sites-available/searchtube.conf ]; then
	apache-setup.sh
fi

a2ensite searchtube
a2ensite searchtube-le-ssl

service apache2 start


while :
do
	echo "Proccessing channels"
	proccess_channels
	echo "Slepping"
	sleep 6h
done
