#!/bin/bash
set -e -x
tar -xzvf archive-$(date +%F).tar.gz
mkdir -p dec_db/Multi
cd db

mapfile -t db_file_list < <(ls | grep db)
for i in "${db_file_list[@]}"; do
    ../decrypt $i
done

mv dec*.db ../dec_db/

cd Multi
mapfile -t db_file_list < <(ls | grep db)
for i in "${db_file_list[@]}"; do
    ../../decrypt $i
done
mv dec*.db ../../dec_db/Multi/

cd ../..
rm archive-$(date +%F).tar.gz
