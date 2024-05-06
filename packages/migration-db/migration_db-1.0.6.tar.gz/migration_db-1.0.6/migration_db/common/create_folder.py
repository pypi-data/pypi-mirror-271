#!/usr/bin/python3
# -*- coding:utf-8 -*-
# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 7/31/2023 3:03 PM
@Description: Description
@File: compare_two_dict.py
"""
import os
import warnings

from .log import Logger


def _create_folder(base_url, name):
    create_path = base_url + "/" + name
    os.makedirs(create_path)
    Logger().info(f"Create folder::{create_path} successfully.")


def create_folder(base_url, name=None):
    warnings.warn("create_folder is deprecated.", DeprecationWarning)
    if not os.path.isabs(base_url):
        raise Exception(f"The path({base_url}) is not a full path.")
    base_url = base_url.replace("\\", "/")
    folders = list()
    while not os.path.exists(base_url):
        spilt_list = base_url.split("/")
        base_url = "/".join(spilt_list[:-1])
        folders.insert(0, spilt_list[-1])
    if folders:
        for folder in folders:
            _create_folder(base_url, folder)
            base_url += f"/{folder}"
    if not name:
        return
    project_dir = os.listdir(base_url)
    if name not in project_dir:
        _create_folder(base_url, name)
