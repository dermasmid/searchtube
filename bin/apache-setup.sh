#!/bin/bash

source .env

cat << EOF > /etc/apache2/sites-available/searchtube.conf
<VirtualHost *:80>
        ServerName $SERVER_NAME
        ServerAdmin $SERVER_ADMIN
        WSGIScriptAlias / /var/www/searchtube/web/searchtube.wsgi
        <Directory /var/www/searchtube/>
                Require all granted

        </Directory>
        Alias /static /var/www/searchtube/web/static
        <Directory /var/www/searchtube/web/static/>
                Require all granted

        </Directory>
        ErrorLog /var/log/apache2/error.log
        LogLevel warn
        CustomLog /var/log/apache2/access.log combined
        SetEnv DB_USERNAME $DB_USERNAME
        SetEnv DB_PASSWORD $DB_PASSWORD
</VirtualHost>
EOF
