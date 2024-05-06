# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/6/2024 9:54 AM
@Description: Description
@File: backup.py
"""
import os
import sys
import zipfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from common.conf.data_source_route import DataSourceRoute
from migration.lib.mysql_task import MysqlTask
from migration.lib.path import build_sql_file_path


def backup(dir_path, host_alias, db_name, sql_name, _is_compress=False, data_source=None):
    local_sql_path = build_sql_file_path(dir_path, sql_name)
    if data_source is None:
        data_source = DataSourceRoute().build_config(host_alias, use_config_obj=False)
    data_source["db"] = db_name
    MysqlTask(**data_source).mysqldump_task(local_sql_path)
    if _is_compress is True:
        zip_backup_path = os.path.join(dir_path, sql_name + ".zip")
        with zipfile.ZipFile(zip_backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(local_sql_path, arcname=sql_name + ".sql")
        if os.path.exists(local_sql_path):
            os.remove(local_sql_path)
