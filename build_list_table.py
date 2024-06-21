# -*- coding: utf-8 -*-

from rstobj import ListTable, Image


data = [
    (
        "acore_constants",
        "AzerothCore World of Warcraft server project constants variables.",
    ),
    (
        "acore_paths",
        "Azerothcore World of Warcraft Server File / Folder structure definition.",
    ),
    (
        "acore_conf",
        "Azerothcore WOW ``authserver.conf``, ``worldserver.conf`` file management.",
    ),
    ("acore_server_metadata", "Azerothcore WOW server metadata for Fleet management."),
    (
        "acore_server_config",
        "Azerothcore World of Warcraft fleet of Servers configuration management.",
    ),
    (
        "acore_server",
        "AzerothCore World of Warcraft logical server data model, and per server level operation.",
    ),
    (
        "acore_soap_app",
        "Azerothcore World of Warcraft Soap Remote Access Python Library.",
    ),
    (
        "acore_db_ssh_tunnel",
        "Create Database SSH Tunnel for Azerothcore World of Warcraft MySQL Database.",
    ),
    ("acore_db_app", "Azerothcore World of Warcraft Database Application."),
    (
        "acore_server_bootstrap",
        "Bootstrap an EC2 instance with the latest Azerothcore core to be game play ready.",
    ),
]


def slugify(name) -> str:
    return name.replace("_", "-")


ltable_data = [
    (
        "Package",
        "Description",
        "Document",
        "Version",
        "CI",
    )
]
tab = "            "
ltable_data_1 = [
    (
        f"`{name} <https://github.com/MacHu-GWU/{name}-project>`_",
        description,
        f".. image:: https://readthedocs.org/projects/{slugify(name)}/badge/?version=latest\n{tab}:target: https://{slugify(name)}.readthedocs.io/en/latest/",
        f".. image:: https://img.shields.io/pypi/v/{slugify(name)}.svg\n{tab}:target: https://pypi.python.org/pypi/{slugify(name)}",
        f".. image:: https://github.com/MacHu-GWU/{name}-project/actions/workflows/main.yml/badge.svg\n{tab}:target: https://github.com/MacHu-GWU/{name}-project/actions?query=workflow:CI",
    )
    for name, description in data
]
ltable_data.extend(ltable_data_1)
ltable = ListTable(
    data=ltable_data,
    title="Title",
    header=True,
)
print(ltable.render())
