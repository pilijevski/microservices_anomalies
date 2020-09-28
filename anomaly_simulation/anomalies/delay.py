from .anomaly import PumbaAnomaly


class DelayAnomaly(PumbaAnomaly):
    def __init__(self, config, name=""):
        self.pumba_command = "delay"
        super().__init__(config, name)
