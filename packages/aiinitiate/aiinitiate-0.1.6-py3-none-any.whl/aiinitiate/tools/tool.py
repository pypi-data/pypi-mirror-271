import typer
from typer import echo
import os
import shutil
from ..config import TOOLS_DIR
from .downloader import download
from .setter import gen_setter


class Tool:
    name: str
    filename: str
    download_url: str
    type: str
    params: dict
    status: dict

    def __init__(self, name, filename, download_url, type, params: dict = {}, status: dict = {}):
        self.name = name
        self.filename = filename
        self.download_url = download_url
        self.type = type
        self.params = params
        self.status = status
        self._on_change_callback = None

        self._tool_dir = os.path.join(TOOLS_DIR, self.name)
        self._save_path = os.path.join(self._tool_dir, self.filename)
        os.makedirs(self._tool_dir, exist_ok=True)

        # 设置器
        self.setter = gen_setter(self)

    def to_dict(self):
        return {
            "name": self.name,
            "filename": self.filename,
            "download_url": self.download_url,
            "type": self.type,
            "params": self.params,
            "status": self.status
        }

    def set_on_change_callback(self, callback):
        self._on_change_callback = callback

    def init(self):
        if not self.status.get("initialized", False):
            self._download()
            self.setter.init(params=self.params)
            self.status["initialized"] = True
            self._on_change_callback()

    def force_download(self):
        self._download(force=True)

    def reset(self):
        shutil.rmtree(self._tool_dir, ignore_errors=True)
        self.setter.reset()
        self.status["initialized"] = False
        self._on_change_callback()

    def handle_action(self, action: str = "", params: dict={}):
        print(f"[handle action] action: {action} params: {params}")
        return self.setter.handle_action(action, params)

    def list_action(self):
        actions = self.setter.list_action()
        typer.echo(f"{self.name} action list:")
        for action in actions:
            typer.echo(f"{action}")
        return actions

    def _download(self, force=False):
        if os.path.exists(self._save_path) and not force:
            echo(f"{self.name} already exist and does not need to download.")
            return
        echo(f"start download {self.name}")
        try:
            download(self.download_url, save_path=self._save_path)
        except Exception as e:
            echo(str(e))
        echo(f"{self.name} download success!")
