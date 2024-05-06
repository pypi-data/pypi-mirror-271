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
from migration.core.execute_script import ExecuteScript
from migration.lib.mysql_task import MysqlTask
from migration.lib.path import build_sql_file_path


def backup(dir_path: str, sql_name, is_compress=False, data_source=None, host_alias=None):
    local_sql_path = build_sql_file_path(dir_path, sql_name)
    if data_source is None and host_alias is not None:
        data_source = DataSourceRoute().build_config(host_alias, use_config_obj=False)
    if data_source is None:
        raise Exception("Please set the data source.")
    MysqlTask(**data_source).mysqldump_task(local_sql_path)
    if is_compress is True:
        zip_backup_path: str = os.path.join(dir_path, sql_name + ".zip")
        with zipfile.ZipFile(zip_backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(local_sql_path, arcname=sql_name + ".sql")
        if os.path.exists(local_sql_path):
            os.remove(local_sql_path)
    print("Back up database successfully.")


def mgmt_schema_history_and_backup(dir_path: str, sql, is_compress, data_source, latest_version_id, host_alias=None):
    ExecuteScript(data_source).init_schema_history_and_latest_sql_version(latest_version_id)
    backup(dir_path, sql, is_compress, data_source, host_alias)
