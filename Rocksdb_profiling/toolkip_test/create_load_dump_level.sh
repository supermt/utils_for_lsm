#!/bin/bash

echo "create the /tmp/dump"
./create_temp_dbdump.py
echo "clean the directory"
rm -rf /tmp/test_db_new load/*
echo "loading by ldb_tool"
cat /tmp/dbdump | ./ldb --db=/tmp/test_db_new load --block_size=65536 --create_if_missing --disable_wal
echo "data processing"
./sst_dump --file=/tmp/test_db_new --command=raw
