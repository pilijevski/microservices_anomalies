from .anomaly import PumbaAnomaly


class PacketLossAnomaly(PumbaAnomaly):
    def __init__(self, config, name=""):
        self.pumba_anomaly = "loss"
        super().__init__(config, name)
