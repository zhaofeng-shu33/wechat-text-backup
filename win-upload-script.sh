#!/bin/bash
user=~/Documents/"WeChat Files"/zhaofeng_shu33/Msg
mkdir -p db/Multi
find "$user" -name "*.db" | xargs -d '\n' cp -t db
find "$user"/Multi/ -name "*.db" | xargs -d '\n' cp -t db/Multi
tar -czvf archive-$(date +%F).tar.gz db
if [ -f ".upload.sh" ]; then
    bash .upload.sh
fi
