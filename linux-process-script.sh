#!/bin/bash
if [ -f ".upload.sh" ]; then
    bash .upload.sh
fi
set -e -x
tar -xzvf archive-$(date +%F).tar.gz

mkdir -p dec_db/Multi

mapfile -t db_file_list < <(find db/ -name "*.db")
for i in "${db_file_list[@]}"; do
    ./decrypt $i
    mv $i.dec.db dec_$i.dec.db &
done


# rm archive-$(date +%F).tar.gz
