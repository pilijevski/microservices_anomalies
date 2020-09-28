import os
from datetime import datetime
from base import Runnable


class Anomaly(Runnable):
    def __init__(self, config, name=""):
        self.timeout = 0
        self.name = name
        self.config = config
        self.exec_string = ""
        self.start_time, self.end_time = None, None

    def _construct_exec_string(self):
        return self.exec_string

    def run(self):
        return self.run_anomaly()

    def run_anomaly(self):
        self.start_time = datetime.utcnow()
        print(f"{self.start_time} {self.exec_string}")
        os.system(self.exec_string)
        self.end_time = datetime.utcnow()
        return self

    def store_results(self):
        pass


class PumbaAnomaly(Anomaly):
    def __init__(self, config, name=""):
        super().__init__(config, name)
        self.pumba_command = self.pumba_command or "delay"
        self.config = self.parse_config(config['config'])
        self._construct_exec_string()

    def _construct_exec_string(self):
        self.exec_string = " ".join(["pumba",
                                     "netem",
                                     self.config["global_options"],
                                     self.pumba_command,
                                     self.config["command_options"],
                                     self.config["containers"]])
        print(self.exec_string)

    @staticmethod
    def parse_config(config):
        parsed_config = dict()
        for key, params in config.items():
            if type(params) == dict:
                parsed_config[key] = " ".join(f"--{sub_key} {sub_param}" for sub_key, sub_param in params.items())
            else:
                parsed_config[key] = params
        return parsed_config
