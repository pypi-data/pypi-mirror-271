import os
import sys
from typing import Any, Iterable, Type

from typer import Typer

from infrable import errors
from infrable.host import Host
from infrable.meta import Meta
from infrable.service import Service
from infrable.switch import Switch

INFRA_MODULE_NAME = "infra"

items: dict[str, Any] = {}
item_types: dict[Type[Any], dict[str, Any]] = {}

hosts: dict[str, Host] = {}
services: dict[str, Service] = {}
host_groups: dict[str, list[Host]] = {}
switches: dict[str, Switch] = {}
typers: dict[str, Typer] = {}
metas: dict[str, Meta] = {}

by_fqdn: dict[str, Host] = {}
by_ip: dict[str, Host] = {}


if not items:
    if not os.path.exists(f"{INFRA_MODULE_NAME}.py"):
        raise errors.InfraDotPyNotFoundError(INFRA_MODULE_NAME)

    sys.path.append(".")
    infra_module = __import__(INFRA_MODULE_NAME)

    for name in dir(infra_module):
        if name.startswith("_"):
            # Skip private members
            continue
        item = getattr(infra_module, name)
        if type(item) == type:
            # Skip classes
            continue

        items[name] = item
        itemtype = type(item)
        if itemtype not in item_types:
            item_types[itemtype] = {}
        item_types[itemtype][name] = item

        if isinstance(item, Host):
            hosts[name] = item
            by_ip[item.ip] = item
            if item.fqdn:
                by_fqdn[item.fqdn] = item
            if item.typer:
                typers[name] = item.typer
        elif isinstance(item, Service):
            services[name] = item
            if item.typer:
                typers[name] = item.typer
                continue
        elif isinstance(item, Switch):
            switches[name] = item
            if item.typer:
                typers[name] = item.typer
            continue
        elif isinstance(item, Meta):
            metas[name] = item
            if "typer" in item:
                typers[name] = item.typer
            continue
        elif isinstance(item, Typer):
            typers[name] = item
            continue
        elif isinstance(item, list) and item and isinstance(item[0], Host):
            host_groups[name] = item
            continue
        elif t := getattr(item, "typer", None):
            if isinstance(t, Typer):
                typers[name] = t
            continue
        else:
            continue


def get_host(name: str) -> Host | None:
    """Get a host by name, FQDN, IP or service name."""

    if host := hosts.get(name) or by_fqdn.get(name) or by_ip.get(name):
        return host
    if host := services.get(name):
        return host.host
    return None


def filtered_hosts(only: Iterable[str] | None = None) -> Iterable[Host]:
    """Filter hosts by name, FQDN, IP, service name or host group."""

    if not only:
        return hosts.values()

    for o in only or []:
        if item := get_host(o):
            yield item
        elif item := host_groups.get(o):
            for h in item:
                yield h
        else:
            raise errors.HostOrServiceNotFoundError(o)
