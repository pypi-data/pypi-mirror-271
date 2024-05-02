builtins = [
    {
        "name": "filebrowser",
        "filename": "filebrowser.tar",
        "download_url": "https://nbstore.oss-cn-shanghai.aliyuncs.com/image/filebrowser.tar",
        "type": "docker",
        "status": {"initialized": False},
        "params": {
            "__docker_run_params": {
                "image": "filebrowser/filebrowser:s6",
                "name": "filebrowser",
                "ports": {"80/tcp": 8888},
                "restart_policy": {"Name": "unless-stopped"},
                "volumes": {
                    '/': {'bind': '/srv', 'mode': 'rw'},
                    "~/.rock/tools/filebrowser/database": {'bind': '/database', 'mode': 'rw'},
                    "~/.rock/tools/filebrowser/config": {'bind': '/config', 'mode': 'rw'}
                },
                "environment": {
                    'PUID': "$UID",
                    'PGID': "$GID"
                }
            },
        }
    },
    {
        "name": "coral-gateway",
        "filename": "coral-gateway.tar",
        "download_url": "https://nbstore.oss-cn-shanghai.aliyuncs.com/image/coral-gateway.tar",
        "type": "docker",
        "status": {"initialized": False},
        "params": {
            "__docker_run_params": {
                "image": "kefei/coral-gateway",
                "name": "coral-gateway",
                "ports": {"8000/tcp": 8000},
                "restart_policy": {"Name": "unless-stopped"},
                "volumes": {
                    "~/.coral": {"bind": "/root/.coral", "mode": "rw"},
                    "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"},
                },
                "environment": {
                    "CORAL_GATEWAY_CONFIG": "eyJtcXR0IjogeyJicm9rZXIiOiAiNDcuMTE2LjE0Ljg1IiwgInBvcnQiOiA5MDIyLCAidXNlcm5hbWUiOiAiYWRtaW4iLCAicGFzc3dvcmQiOiAiYWRtaW4ifSwgImdhdGV3YXlfaWQiOiAiY29yYWwtY2hhbmdlLWdhdGV3YXkiLCAib3JnYW5pemF0aW9uX2lkIjogImNvcmFsLWNoYW5nZS11c2VyIn0=",
                    "CORAL_GATEWAY_PUBLIC_IP": "47.116.14.85",
                    "CORAL_GATEWAY_PORT": "$REMOTE_PORT_FOR_CORAL_GATEWAY",
                    "CORAL_DEVICE_SSH_PORT": 22,
                    "CORAL_DEVICE_TYPE": "$DEVICE_TYPE",
                    "CORAL_DEVICE_ID": "$MAC_ADDR"
                }
            }
        }
    }
]


def _on_frpc_init():
    # 默认将ssh 22端口 注册进配置文件
    from .. import g
    g.add_frpc_proxies("ssh", 22)
    g.enable_frpc()


def _on_coral_gateway_init():
    from .. import g
    g.add_frpc_proxies("coral_gateway", 8000)


def _on_filebrowser_init():
    # 将8888端口注册到配置文件
    from .. import g
    g.add_frpc_proxies("filebrowser", 8888)


builtin_init_function_dict = {
    "frpc": _on_frpc_init,
    "filebrowser": _on_filebrowser_init,
    "coral-gateway": _on_coral_gateway_init,
}


def on_builtin_init(name):
    builtin_init_function_dict.get(name)()
