#!/bin/sh


service apache2 start


while :
do
	echo "Proccessing channels"
	proccess_channels
	echo "Slepping"
	sleep 6h
done
