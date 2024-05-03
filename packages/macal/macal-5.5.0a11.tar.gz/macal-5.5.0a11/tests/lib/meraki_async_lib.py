# -*- coding: utf-8 -*-
#
# Product:   Meraki Async Library
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-03-31
#
# Copyright 2024 Westcon-Comstor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT
#

import sys
import time

from typing import Callable, Optional, Union, Any
import asyncio
from asyncio import Future
from meraki.aio import AsyncDashboardAPI  # type: ignore


ma_task_result = Union[dict, Exception]
ma_task_list_result = Future[dict[str, Any]]


class ma_task:
    def __init__(self, task: Callable):
        self.task = task


class ma_org_task(ma_task):
    def __init__(self, org_id: str, task: Callable):
        super().__init__(task)
        self.org_id = org_id


class ma_dev_task(ma_task):
    def __init__(self, serial: str, task: Callable):
        super().__init__(task)
        self.serial = serial


class ma_net_task(ma_task):
    def __init__(self, network_id: str, task: Callable):
        super().__init__(task)
        self.network_id = network_id


class async_task_list:
    def __init__(self, api_key: str) -> None:
        self._tasks: list[ma_task] = []
        self._org_tasks: list[ma_org_task] = []
        self._dev_tasks: list[ma_dev_task] = []
        self._net_tasks: list[ma_net_task] = []
        self._task_names: list[str] = []
        self._api_key: str = api_key
        self.max_concurrent_tasks: int = 10  # rate limiting

    def add_task(self, task: Callable):
        if not asyncio.iscoroutinefunction(task):
            raise ValueError("Task must be an async function")
        self._task_names.append(task.__name__)
        self._tasks.append(ma_task(task))

    def add_org_task(self, org_id: str, task: Callable):
        if not asyncio.iscoroutinefunction(task):
            raise ValueError("Task must be an async function")
        self._task_names.append(task.__name__)
        self._org_tasks.append(ma_org_task(org_id, task))

    def add_dev_task(self, serial: str, task: Callable):
        if not asyncio.iscoroutinefunction(task):
            raise ValueError("Task must be an async function")
        self._task_names.append(task.__name__ + ":" + serial)
        self._org_tasks.append(ma_org_task(serial, task))

    def add_net_task(self, network_id: str, task: Callable):
        if not asyncio.iscoroutinefunction(task):
            raise ValueError("Task must be an async function")
        self._task_names.append(task.__name__ + ":" + network_id)
        self._org_tasks.append(ma_org_task(network_id, task))

    def task_count(self):
        return (
            len(self._tasks)
            + len(self._org_tasks)
            + len(self._dev_tasks)
            + len(self._net_tasks)
        )

    async def run_tasks(self):
        result = {}
        async with AsyncDashboardAPI(
            self._api_key, print_console=False, simulate=True, output_log=False
        ) as client:
            task_list = [task.task(client) for task in self._tasks]
            task_list += [
                org_task.task(client, org_task.org_id) for org_task in self._org_tasks
            ]
            task_list += [
                dev_task.task(client, dev_task.serial) for dev_task in self._dev_tasks
            ]
            task_list += [
                net_task.task(client, net_task.network_id)
                for net_task in self._net_tasks
            ]
            total_batches = (
                len(task_list) + self.max_concurrent_tasks - 1
            ) // self.max_concurrent_tasks

            for batch_num in range(total_batches):
                start_time = time.perf_counter()
                start_idx = batch_num * self.max_concurrent_tasks
                end_idx = min(
                    (batch_num + 1) * self.max_concurrent_tasks, len(task_list)
                )
                batch = task_list[start_idx:end_idx]
                batch_result = await asyncio.gather(*batch, return_exceptions=True)
                elapsed_time = time.perf_counter() - start_time
                if elapsed_time < 1.1:
                    time.sleep(1.1 - elapsed_time)
                for i in range(len(batch_result)):
                    task_name = self._task_names[start_idx + i]
                    result[task_name] = batch_result[i]

        return result

    def run(self) -> ma_task_list_result:
        time.sleep(1)
        result = asyncio.run(self.run_tasks())
        return result


global_task_list: Optional[async_task_list] = None


def init_task_list(api_key: str):
    global global_task_list
    global_task_list = async_task_list(api_key=api_key)
    return None


def add_task(task: Callable):
    global global_task_list
    if global_task_list is not None:
        global_task_list.add_task(task)


def add_org_task(org_id: str, task: Callable):
    global global_task_list
    if global_task_list is not None:
        global_task_list.add_org_task(org_id=org_id, task=task)


def add_dev_task(serial: str, task: Callable):
    global global_task_list
    if global_task_list is not None:
        global_task_list.add_dev_task(serial=serial, task=task)


def add_net_task(network_id: str, task: Callable):
    global global_task_list
    if global_task_list is not None:
        global_task_list.add_net_task(network_id=network_id, task=task)


def run_tasks() -> dict[str, Any]:
    global global_task_list
    flag = False
    if global_task_list is None:
        raise ValueError("Task list not initialized")
    data: ma_task_list_result = global_task_list.run()
    result: dict[str, Any] = {}
    if data is None or not isinstance(data, dict):
        raise ValueError("Task list did not return a dictionary")
    for key, row in data.items():
        if row is None:
            continue
        if "get_app_device_performance" in key:
            if result.get("get_app_device_performance", None) is None:
                result["get_app_device_performance"] = []
            row_data = {k: v for k, v in row.items()}
            row_data["serial"] = key.split(":")[1]
            result["get_app_device_performance"].append(row_data)
        elif "get_switch_device_ports_statuses" in key:
            if result.get("get_switch_device_ports_statuses", None) is None:
                result["get_switch_device_ports_statuses"] = []
            row_data = {}
            row_data["serial"] = key.split(":")[1]
            row_data["portstates"] = row
            result["get_switch_device_ports_statuses"].append(row_data)
        else:
            result[key] = row
    if flag:
        sys.exit(1)
    return result


# Global organizations wide tasks
async def get_orgs(client: AsyncDashboardAPI) -> ma_task_result:
    return await client.organizations.getOrganizations()


# Organization specific tasks
async def get_org(client: AsyncDashboardAPI, org_id: str) -> ma_task_result:
    return await client.organizations.getOrganization(org_id)


async def get_org_inventory(client: AsyncDashboardAPI, org_id: str) -> ma_task_result:
    return await client.organizations.getOrganizationInventoryDevices(
        org_id, total_pages="all"
    )


async def get_org_devices(client: AsyncDashboardAPI, org_id: str) -> ma_task_result:
    return await client.organizations.getOrganizationDevices(org_id, total_pages="all")


async def get_org_networks(client: AsyncDashboardAPI, org_id: str) -> ma_task_result:
    return await client.organizations.getOrganizationNetworks(org_id, total_pages="all")


async def get_org_devices_statuses(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.organizations.getOrganizationDevicesStatuses(
        org_id, total_pages="all"
    )


async def get_org_config_templates(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.organizations.getOrganizationConfigTemplates(org_id)


async def get_org_licenses_overview(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.organizations.getOrganizationLicensesOverview(org_id)


async def get_org_licenses(client: AsyncDashboardAPI, org_id: str) -> ma_task_result:
    return await client.organizations.getOrganizationLicenses(org_id, total_pages="all")


async def get_org_devices_uplinks_loss_and_latency(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.organizations.getOrganizationDevicesUplinksLossAndLatency(
        org_id, total_pages="all"
    )


async def get_app_org_uplink_statuses(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.appliance.getOrganizationApplianceUplinkStatuses(
        org_id, total_pages="all"
    )


async def get_app_org_vpn_statuses(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.appliance.getOrganizationApplianceVpnStatuses(
        org_id, total_pages="all"
    )


async def get_app_org_vpn_stats(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.appliance.getOrganizationApplianceVpnStats(
        org_id, total_pages="all"
    )


async def get_org_app_uplinks_usage_by_network(
    client: AsyncDashboardAPI, org_id: str
) -> ma_task_result:
    return await client.appliance.getOrganizationApplianceUplinksUsageByNetwork(
        org_id, timespan=600, total_pages="all", resolution=600
    )


# device specific tasks:


async def get_app_device_performance(
    client: AsyncDashboardAPI, serial: str
) -> ma_task_result:
    return await client.appliance.getDeviceAppliancePerformance(
        serial, total_pages="all"
    )


async def get_switch_device_ports_statuses(
    client: AsyncDashboardAPI, serial: str
) -> ma_task_result:
    return await client.switch.getDeviceSwitchPortsStatuses(serial=serial, timespan=300)


# network specific tasks:


async def get_app_network_appliance_uplinks_usage_history(
    client: AsyncDashboardAPI, network_id: str
) -> ma_task_result:
    return await client.appliance.getNetworkApplianceUplinksUsageHistory(
        networkId=network_id, resolution=60, timespan=600, total_pages="all"
    )


def process_loss_and_latency(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for row in data:
        new_row = {k: v for k, v in row.items() if k != "timeSeries"}
        ts = row.get("timeSeries", [])
        loss = 0.0
        latency = 0.0
        count = 0
        for t in ts:
            lp = t.get("lossPercent", 0.0)
            lm = t.get("latencyMs", 0.0)
            if lp == "nil":
                lp = 0.0
            if lm == "nil":
                lm = 0.0
            loss += float(lp)
            latency += float(lm)
            count += 1
        new_row["lossPercent"] = loss / count
        new_row["latencyMs"] = latency / count
        result.append(new_row)
    return result
