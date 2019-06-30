#!/bin/bash

cd /home/website/gowashing/
echo `pwd`
webpid_msg="webPid"
kill_msg="kill web.pid...."

echo ${webpid_msg}: `cat web.pid`
kill `cat web.pid`
echo ${kill_msg}
git pull
echo 'git pull success....'

source /home/website/env/bin/activate
gunicorn application:app -p web.pid -D
echo ${webpid_msg}:`cat web.pid`