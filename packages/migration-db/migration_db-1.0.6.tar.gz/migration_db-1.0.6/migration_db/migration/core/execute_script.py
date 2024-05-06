# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 6/27/2022 10:46 AM
@Description: Description
@File: execute_script.py
"""
import os
import time

from common.format_time import now_utc
from common.handle_str import ParseBizSqlForAppInfo
from common.path import incremental_sql_dir_path
from migration.db.base_db import BaseDb
from migration.lib.constant import TABLE_SCHEMA_HISTORY
from migration.lib.mysql_task import MysqlTask
from migration.lib.path import common_sql_path


class ExecuteScript:

    def __init__(self, app_db_route, app):
        self.app_db_route = app_db_route
        self.app = app

    def execute_incremental_sql(self, ignore_error=False, latest_version=None):
        sql_dir = os.path.join(incremental_sql_dir_path(), self.app)
        all_tables = BaseDb(self.app_db_route).get_all_tables()
        if TABLE_SCHEMA_HISTORY not in all_tables:
            table_schema_path = os.path.join(common_sql_path(), "{0}.sql".format(TABLE_SCHEMA_HISTORY))
            MysqlTask(**self.app_db_route).mysql_task(table_schema_path)
        sql = "SELECT script FROM eclinical_schema_history WHERE type='SQL' " \
              "AND success=TRUE ORDER BY installed_rank DESC LIMIT 1;"
        item = BaseDb(self.app_db_route).fetchone(sql)
        db_max_version = None
        if item is not None:
            script = item.get("script")
            p = ParseBizSqlForAppInfo().parse(script)
            db_max_version = p.version_id
        if db_max_version is None or db_max_version == latest_version:
            return
        version_file_mapping = dict()
        for root, dirs, files in os.walk(sql_dir):
            for sql_name in files:
                if not sql_name.endswith('.sql'):
                    continue
                p = ParseBizSqlForAppInfo().parse(sql_name)
                version = p.version_id
                if (latest_version is not None and version > latest_version) or version <= db_max_version:
                    continue
                version_file_mapping.update({version: sql_name})
        version_file_mapping = sorted(version_file_mapping.items(), key=lambda s: s[0])
        for version, sql_name in version_file_mapping:
            is_execute = False
            try:
                item = BaseDb(self.app_db_route).fetchone(
                    f"SELECT * FROM eclinical_schema_history WHERE script='{sql_name}';")
            except Exception as e:
                raise Exception(e)
            if not item:
                if db_max_version and version > db_max_version:
                    is_execute = True
                elif db_max_version is None:
                    is_execute = True
                try:
                    if is_execute:
                        sql_path = os.path.join(sql_dir, sql_name)
                        MysqlTask(**self.app_db_route).mysql_task(sql_path)
                        success = True
                    else:
                        continue
                except Exception as e:
                    success = False
                    if ignore_error is False:
                        raise Exception(e)
                # insert the sql executed record
                if success is False:
                    continue
                max_item = BaseDb(self.app_db_route).fetchone(
                    f"SELECT installed_rank FROM eclinical_schema_history ORDER BY installed_rank DESC LIMIT 1;")
                max_id = max_item.get('installed_rank') if max_item else 0
                BaseDb(self.app_db_route).insert(
                    "eclinical_schema_history",
                    dict(installed_rank=max_id + 1, version=version, type="SQL", script=sql_name, checksum=0,
                         execution_time=0, description=f"{self.app} business schema incremental sql",
                         installed_by="test_platform", installed_on=now_utc(time.time()), success=1))

    def init_schema_history_and_latest_sql_version(self, latest_version_id):
        if latest_version_id is None:
            return
        all_tables = BaseDb(self.app_db_route).get_all_tables()
        if TABLE_SCHEMA_HISTORY not in all_tables:
            table_schema_path = os.path.join(common_sql_path(), "{0}.sql".format(TABLE_SCHEMA_HISTORY))
            MysqlTask(**self.app_db_route).mysql_task(table_schema_path)
        sql = "SELECT * FROM eclinical_schema_history WHERE type='SQL' " \
              "AND success=TRUE ORDER BY installed_rank DESC LIMIT 1;"
        item = BaseDb(self.app_db_route).fetchone(sql)
        db_max_version = None
        installed_rank = 0
        if item is not None:
            script = item.get("script")
            installed_rank = item.get("installed_rank")
            p = ParseBizSqlForAppInfo().parse(script)
            db_max_version = p.version_id
        flag = False
        if db_max_version is None:
            flag = True
        elif db_max_version < latest_version_id:
            flag = True
        if flag:
            # insert the latest sql_version
            sql_name = f"V{latest_version_id}__{self.app}_business_schema_incremental_sql.sql"
            BaseDb(self.app_db_route).insert(
                "eclinical_schema_history",
                dict(installed_rank=installed_rank + 1, version=latest_version_id, type="SQL", script=sql_name,
                     checksum=0, execution_time=0, description=f"{self.app} business schema incremental sql",
                     installed_by="test_platform", installed_on=now_utc(time.time()), success=1))
