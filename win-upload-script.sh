#!/bin/bash
user=~/Documents/"WeChat Files"/zhaofeng_shu33/Msg
rm -rf db
mkdir -p db/Multi
cp "$user"/MicroMsg.db db/
cp "$user"/Multi/MSG0.db db/Multi/MSG0.db
cp "$user"/Multi/MSG1.db db/Multi/MSG1.db
tar -czvf archive-$(date +%F).tar.gz db
if [ -f ".upload.sh" ]; then
    bash .upload.sh
fi
