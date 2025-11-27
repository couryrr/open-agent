import json
import os
from platformdirs import user_config_dir, user_data_dir
from pydantic import BaseModel

from .provider import OpenRunnerProvider
from .session import OpenRunnerSession


class OpenRunnerState(BaseModel):
    appname: str = "openrunner"
    appauthor: str = "nextbubble"
    config: dict[str, str] = {"data_dir": user_data_dir(appname, appauthor)}
    sessions: dict[str, OpenRunnerSession] = {}
    providers: dict[str, OpenRunnerProvider] = {}

    def load_config(self):
        config_dir = user_config_dir(self.appname, self.appauthor)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            with open(os.path.join(config_dir, "config.json"), "w") as file:
                file.write("{}")
        with open(os.path.join(config_dir, "config.json"), "r") as file:
            self.config = json.load(file)

    def save(self):
        with open(os.path.join(self.config["data_dir"], "data.json"), "w") as file:
            file.write(self.model_dump_json())

