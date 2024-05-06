# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/6/2024 9:51 AM
@Description: Description
@File: backup_by_database.py
"""
import threading
import time

from common.conf.constant import TestEnv
from common.format_time import now_yyyy_mm_dd
from migration.core.backup import backup

if __name__ == '__main__':
    sql_dir = r"D:\Temp-own"
    target_host = TestEnv.dev01
    is_compress = True
    databases = [
        "eclinical_edc_dev_820"
    ]
    for database in databases:
        sql_name = "_".join([database, target_host, now_yyyy_mm_dd(time.time()), "V76_upgraded11"])
        t = threading.Thread(target=backup, args=(sql_dir, target_host, database, sql_name, is_compress))
        t.start()
        print(f"The thread::{threading.current_thread().ident} start.")
