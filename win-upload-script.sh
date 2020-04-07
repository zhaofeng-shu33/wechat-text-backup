#!/bin/bash
user=~/Documents/"WeChat Files"/zhaofeng_shu33/Msg
mkdir -p db/Multi
find "$user" -name "*.db" | xargs -d '\n' cp -t db
tar -czvf archive-$(date +%F).tar.gz db

