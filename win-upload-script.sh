#!/bin/bash
user=~/Documents/"WeChat Files"/zhaofeng_shu33/Msg
rm -rf db
mkdir -p db/Multi
cp "$user"/MicroMsg.db db/

mapfile -t db_file_list < <(ls Multi | grep ^MSG[0-9].db$)
for i in "${db_file_list[@]}"; do
    cp "$user"/Multi/$i db/Multi/$i
done

tar -czvf archive-$(date +%F).tar.gz db
if [ -f ".upload.sh" ]; then
    bash .upload.sh
fi
