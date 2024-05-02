from .base import Setter, DockerSetter, BinarySetter


def gen_setter(tool) -> Setter:
    setter = None
    if tool.type == "binary":
        setter = BinarySetter(tool)
    elif tool.type == "docker":
        setter = DockerSetter(tool)
    return setter
