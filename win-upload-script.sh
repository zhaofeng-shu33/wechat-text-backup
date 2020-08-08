#!/bin/bash
user=~/Documents/"WeChat Files"/zhaofeng_shu33/Msg
mkdir -p db/Multi
cp "$user"/MicroMsg.db.dec.db db/
cp "$user"/Multi/MSG0.db.dec.db db/Multi/
tar -czvf archive-$(date +%F).tar.gz db
if [ -f ".upload.sh" ]; then
    bash .upload.sh
fi
