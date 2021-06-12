#!/bin/bash

source .env

cat << EOF > /etc/apache2/sites-available/rextube.conf
<VirtualHost *:80>
        ServerName $SERVER_NAME
        ServerAdmin $SERVER_ADMIN
        WSGIScriptAlias / /var/www/rextube/web/rextube.wsgi
        <Directory /var/www/rextube/>
                Require all granted

        </Directory>
        Alias /static /var/www/rextube/web/static
        <Directory /var/www/rextube/web/static/>
                Require all granted

        </Directory>
        ErrorLog /var/log/apache2/error.log
        LogLevel warn
        CustomLog /var/log/apache2/access.log combined
        SetEnv DB_HOST $DB_HOST
        SetEnv DB_USERNAME $DB_USERNAME
        SetEnv DB_PASSWORD $DB_PASSWORD
</VirtualHost>
EOF
