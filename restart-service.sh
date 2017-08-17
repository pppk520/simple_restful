killall -s INT /usr/local/bin/uwsgi
mkdir -p /var/log/uwsgi
mkdir -p /run/uwsgi
uwsgi --ini /tmp/config/uwsgi.ini

if [ -f /etc/nginx/sites-enabled/default ]; then 
    rm /etc/nginx/sites-enabled/default 
fi

service nginx restart

