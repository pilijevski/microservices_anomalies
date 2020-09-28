from .anomaly import PumbaAnomaly


class PacketLossAnomaly(PumbaAnomaly):
    def __init__(self, config):
        self.pumba_command = "cpu_stress"
        super().__init__(config)
