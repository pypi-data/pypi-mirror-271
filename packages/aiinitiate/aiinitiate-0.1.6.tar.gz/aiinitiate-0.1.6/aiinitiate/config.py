import os
import yaml

__DEFAULT_CONFIG_DATA = """
basic:
  frp_server:
    ip: 10.184.13.190
    port: 7500
    auth: YWRtaW46YWRtaW4=
    port_range: [10000, 19999]
"""

# 基础路径
BASE_DIR = os.path.join(os.path.expanduser("~"), ".aiinitiate")
os.makedirs(BASE_DIR, exist_ok=True)
CONFIG_PATH = os.path.join(BASE_DIR, "config.yml")

# 工具路径
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
os.makedirs(TOOLS_DIR, exist_ok=True)

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f.read())
else:
    config = yaml.safe_load(__DEFAULT_CONFIG_DATA)


def dump_config():
    with open(CONFIG_PATH, "w") as f:
        f.write(yaml.safe_dump(config))
