from .anomaly import PumbaAnomaly


class DelayAnomaly(PumbaAnomaly):
    def __init__(self, config, name=""):
        self.pumba_anomaly = "delay"
        super().__init__(config, name)
