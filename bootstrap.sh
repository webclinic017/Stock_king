#!/bin/bash

set -x

# Set local time
export TZ="Asia/Taipei"
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata
# echo -e "nameserver 10.34.1.220\n$(cat /etc/resolv.conf)" > /etc/resolv.conf
export PYTHONPATH=/root/server
crontab -r
python /root/server/startup/set_crontab_script.py
/etc/init.d/cron restart

/usr/bin/supervisord