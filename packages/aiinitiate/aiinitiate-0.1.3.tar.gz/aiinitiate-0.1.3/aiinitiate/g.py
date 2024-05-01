from typing import Dict, List

import typer

from .config import config, dump_config
from .tools.tool import Tool
from .tools.builtin_tools import builtins, on_builtin_init
from .sysinfo import get_mac_address, get_device_model, get_linux_distribution, npu_info


# ---基础函数---
def mac_addr():
    return get_mac_address()


def device_model():
    return get_device_model()


def device_type():
    model = get_device_model()
    _model = model.lower()
    if "rockchip" in _model:
        return "rknn"
    elif "jetson" in _model:
        return "jetson"
    else:
        return "base"


def distribution_name():
    dist_name, _ = get_linux_distribution()
    return dist_name


def distribution_id():
    _, dist_id = get_linux_distribution()
    return dist_id


def npu():
    return npu_info()


# ---tool---
# tools
_tool_dict: Dict[str, Tool] = {}


def on_tool_changed():
    tools = []
    for name in _tool_dict.keys():
        tools.append(get_tool(name).to_dict())
    config["tools"] = tools
    dump_config()


def get_tool(name) -> Tool:
    return _tool_dict.get(name)


def start_tool(name):
    tool = get_tool(name)
    if tool.type == "docker":
        tool.handle_action("container", params={"action": "start"})
    else:
        tool.handle_action("systemctl", params={"action": "start"})


def stop_tool(name):
    tool = get_tool(name)
    if tool.type == "docker":
        tool.handle_action("container", params={"action": "stop"})
    else:
        tool.handle_action("systemctl", params={"action": "stop"})


def restart_tool(name):
    tool = get_tool(name)
    if tool.type == "docker":
        tool.handle_action("container", params={"action": "restart"})
    else:
        tool.handle_action("systemctl", params={"action": "restart"})


def add_tool(name, filename, download_url, type, params: dict = {}, status: dict = {}):
    tool = Tool(name=name, filename=filename, download_url=download_url, type=type, params=params, status=status)
    _tool_dict[tool.name] = tool
    tool.set_on_change_callback(on_tool_changed)
    tool.init()


def list_tool_obj() -> List[Tool]:
    tools = []
    for name in _tool_dict.keys():
        tools.append(_tool_dict.get(name))
    return tools


def add_builtin_tool(name):
    typer.echo(f"start init {name} ===>")
    if name in _tool_dict.keys():
        typer.echo(f"{name} already installed.")
        return
    for item in builtins:
        if item["name"] == name:
            print(f"init Tool: {name}")
            tool = Tool(**item)
            _tool_dict[tool.name] = tool
            tool.set_on_change_callback(on_tool_changed)
            tool.init()
            on_builtin_init(name)
            break
    else:
        raise Exception(f"not found {name} in builtin tools.")


def remove_tool(name):
    _tool_dict.get(name).reset()
    _tool_dict.pop(name)
    on_tool_changed()


def list_tool():
    r = {}
    for item in builtins:
        name = item["name"]
        r[name] = False
    for name in _tool_dict.keys():
        r[name] = True
    tools = []
    for name in r.keys():
        tools.append({"name": name, "installed": r[name]})
    return tools


for tool_item in config.get("tools", []):
    add_tool(**tool_item)
