#!/bin/sh
nginx
/usr/bin/supervisord -c /root/conf/supervisor/super.conf
supervisorctl -c  /root/conf/supervisor/super.conf restart all