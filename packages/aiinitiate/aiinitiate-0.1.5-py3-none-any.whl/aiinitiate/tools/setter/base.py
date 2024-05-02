import os.path

import docker
import typer


class Setter:

    def __init__(self, tool):
        self.tool = tool
        self.tool_dir = tool._tool_dir
        self._action_dict = {}

    def init(self, params: dict):
        pass

    def clear(self):
        pass

    def reset(self):
        pass

    def register_action(self, action, function):
        self._action_dict[action] = function

    def handle_action(self, action: str, action_params: dict = {}):
        if action in self._action_dict.keys():
            return self._action_dict[action](**action_params)
        else:
            raise Exception(f"action {action} is not exist.")

    def list_action(self):
        return self._action_dict.keys()


class BinarySetter(Setter):
    pass


class DockerSetter(Setter):

    def __init__(self, tool):
        super().__init__(tool)
        self.client = docker.from_env()
        _run_params: dict = tool.params.get("__docker_run_params", {})
        self.container_name = _run_params.get("name")

        # 注册操作
        self.register_action("container", self.action_container)

    def init(self, params: dict):
        typer.echo(f"start load docker image {self.tool.name} from: {self.tool._save_path}")
        try:
            self._load_image(image_path=self.tool._save_path)
            typer.echo(f"docker image {self.tool.name} load done.")
        except Exception as e:
            os.remove(self.tool._save_path)
            typer.echo(f"docker image {self.tool.name} load fail.")
            raise e

    def start_container(self):
        typer.echo(f"start run docker container {self.container_name}.")
        container = self._start_container(**self.tool.params.get("__docker_run_params", {}))
        typer.echo(f"docker container {self.container_name} strated (id: {container.id}).")

    def stop_container(self):
        typer.echo(f"stop container: {self.container_name}")
        container = self.client.containers.get(self.container_name)
        container.stop()

    def action_container(self, action):
        if action == "start":
            self.start_container()
        elif action == "stop":
            self.stop_container()
        elif action == "restart":
            try:
                self.stop_container()
            except Exception as e:
                pass
            self.start_container()

    def _load_image(self, image_path):
        # with open(image_path, 'rb') as f:
        #     image_data = f.read()
        # self.client.images.load(image_data)
        os.system(f"docker load -i {image_path}")

    def _start_container(self, **kwargs):
        from ... import g

        print("start container params: ")
        print(kwargs)

        __ENV_VAL_REPLACE_DICT = {
            "$DEVICE_TYPE": g.device_type(),
            "$UID": os.getuid(),
            "$GID": os.getgid(),
            "$MAC_ADDR": g.mac_addr(),
        }

        _volumes_param = kwargs.pop("volumes", {})
        volumes_param = {}
        for host_path in _volumes_param.keys():
            volumes_param[os.path.abspath(host_path)] = _volumes_param.get(host_path)
        kwargs["volumes"] = volumes_param

        _environment_param = kwargs.pop("environment", {})
        environment_param = {}
        for key in _environment_param.keys():
            val = _environment_param.get(key)
            environment_param[key] = __ENV_VAL_REPLACE_DICT.get(val, val)
        kwargs["environment"] = environment_param

        container = self.client.containers.run(detach=True, **kwargs)
        return container
