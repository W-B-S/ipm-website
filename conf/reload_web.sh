#!/bin/sh
default_nginx_conf_path=/etc/nginx/conf.d/hcy.conf
all_nginx_conf_path=/etc/nginx/conf.d/hcy.conf.all
master_nginx_conf_path=/etc/nginx/conf.d/hcy.conf.masteronly
slave_nginx_conf_path=/etc/nginx/conf.d/hcy.conf.slaveronly

# switch to slaveronly
yes|cp $slave_nginx_conf_path $default_nginx_conf_path
nginx -s reload
sleep 3

# sync master
cd /root/workspace/master/
git pull  

master_list=(
master:m0
)
slave_list=(
slave:s0
)
# restart master_list
for item in ${master_list[@]}
    do supervisorctl -c  /root/conf/supervisor/super.conf restart $item
done

sleep 2
# switch to masteronly
yes| cp $master_nginx_conf_path $default_nginx_conf_path
nginx -s reload
sleep 10

# sync slave
cd /root/workspace/slave/
git pull  

# restart slave_list
for item in ${slave_list[@]}
    do supervisorctl -c  /root/conf/supervisor/super.conf restart $item
done

sleep 2
# switch to all
yes| cp $all_nginx_conf_path $default_nginx_conf_path
nginx -s reload