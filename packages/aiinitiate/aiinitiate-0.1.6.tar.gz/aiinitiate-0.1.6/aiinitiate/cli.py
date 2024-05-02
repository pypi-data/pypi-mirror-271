import json, typer
from . import g, __version__
from .basic.common_utils import install_common_utils

app = typer.Typer()


@app.command()
def logo():
    logo = """
    █████  ██ ███████ ██ ███    ██ ██ ████████ ██  ██████  ███    ██ 
    ██   ██ ██ ██      ██ ████   ██ ██      ██    ██    ██  ████   ██ 
    ███████ ██ ███████ ██ ██ ██  ██ ██    ██    ██    ██ ██ ██ ██  ██ 
    ██   ██ ██      ██ ██ ██  ██ ██ ██    ██    ██    ██ ██ ██  ██ ██ 
    ██   ██ ██ ███████ ██ ██   ████ ██    ██     ██████  ██ ██   ████ 
    """
    typer.echo(logo)


@app.command()
def version():
    """
    版本信息
    """
    typer.echo(f"{__version__}")


@app.command()
def setup():
    """
    自动安装各种内置工具
    """
    install_common_utils()

    init_tools = ["filebrowser", "coral-gateway"]
    for name in init_tools:
        # 加载对应工具
        g.add_builtin_tool(name)
        # 启动对应工具
        g.start_tool(name)


@app.command()
def add_tool(name: str):
    """
    下载基础工具到本地
    """
    g.add_builtin_tool(name)


@app.command()
def start_tool(name: str):
    """
    启动工具
    """
    g.start_tool(name)


@app.command()
def stop_tool(name: str):
    """
    停止工具
    """
    g.stop_tool(name)


@app.command()
def restart_tool(name: str):
    """
    重启工具
    """
    g.restart_tool(name)


@app.command()
def remove_tool(name: str):
    """
    删除工具
    """
    g.remove_tool(name)


@app.command()
def handle_tool_action(name: str, action: str, params: str = "{}"):
    tool = g.get_tool(name)
    tool.handle_action(action, json.loads(params))


@app.command()
def list_tool_action(name):
    """
    列出工具支持的操作
    """
    tool = g.get_tool(name)
    tool.list_action()


@app.command()
def list_tool():
    """
    查看工具列表
    :return:
    """
    for item in g.list_tool():
        typer.echo(f"[ {'✅' if item['installed'] else '❎'} ] {item['name']}")


@app.command()
def ip():
    """
    获取设备的内网ip地址
    """
    ip_address = g.local_ip()
    typer.echo(f"Device Local IP Address: {ip_address}")


@app.command()
def public_ip():
    """
    获取设备的公网ip地址
    """
    ip_address = g.public_ip()
    typer.echo(f"Device Public IP Address: {ip_address}")


@app.command()
def mac():
    """
    获取设备的mac地址
    """
    mac_address = g.mac_addr()
    typer.echo(f"Device MAC Address: {mac_address}")


@app.command()
def dist():
    """
    输出系统版本信息
    """
    dist_name = g.distribution_name()
    dist_id = g.distribution_id()
    typer.echo(f"dist id: {dist_id}")
    typer.echo(f"dist name: {dist_name}")


@app.command()
def npu():
    """
    npu信息[仅RK设备支持此命令]
    """
    typer.echo(g.npu())


@app.command()
def device_model():
    """
    获取设备详细型号信息
    """
    typer.echo(g.device_model())


@app.command()
def device_type():
    """
    获取设备类型信息
    """
    typer.echo(g.device_type())


@app.command()
def main():
    logo()
    typer.echo("Welcome to AIInitiate command!")


if __name__ == "__main__":
    app()
