from .anomaly import PumbaAnomaly


class FreezeContainerAnomaly(PumbaAnomaly):
    def __init__(self, config, name=""):
        self.pumba_command = "pause"
        super().__init__(config, name)

    def _construct_exec_string(self):
        self.exec_string = " ".join(["pumba",
                                     self.config["global_options"],
                                     self.pumba_command,
                                     self.config["command_options"],
                                     self.config["containers"]])
        print(self.exec_string)
