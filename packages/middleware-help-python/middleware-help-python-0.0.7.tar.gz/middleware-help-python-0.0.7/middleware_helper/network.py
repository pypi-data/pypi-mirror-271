# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  middleware-help-python
# FileName:     network.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/29
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import psutil


def get_sys_connect() -> list:
    all_connect = list()
    for conn in psutil.net_connections():
        conn_info = dict(
            fd=conn.fd,
            family=dict(name=conn.family.name, value=conn.family.value),
            type=dict(name=conn.type.name, value=conn.type.value),
            status=conn.status,
            pid=conn.pid,
            local_address=conn.laddr.ip,
            local_port=conn.laddr.port,
            remote_address=conn.raddr.ip if len(conn.raddr) > 0 else None,
            remote_port=conn.raddr.port if len(conn.raddr) > 0 else None,
        )
        all_connect.append(conn_info)
    return all_connect


def get_system_port_list() -> dict:
    local_ports = list()
    remote_ports = list()
    for conn in psutil.net_connections():
        local_ports.append(conn.laddr.port)
        if len(conn.raddr) > 0:
            remote_ports.append(conn.raddr.port)
    all_port = dict(local_ports=list(set(local_ports)), remote_ports=list(set(remote_ports)))
    return all_port


def filter_system_port_list(data_port: list, default_port: int) -> int:
    system_port_dict = get_system_port_list()
    local_ports = system_port_dict.get("local_ports")
    remote_ports = system_port_dict.get("remote_ports")
    diff_list_1 = list(set(data_port).difference(set(local_ports)))
    diff_list_2 = list(set(data_port).difference(set(remote_ports)))
    intersection = list(set(diff_list_1).intersection(set(diff_list_2)))
    if len(intersection) > 0:
        port = intersection[0]
    else:
        port = diff_list_1[0] if len(diff_list_1) > 0 else default_port
    return port
