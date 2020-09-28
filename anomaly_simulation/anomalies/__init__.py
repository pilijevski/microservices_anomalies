from .packet_loss import PacketLossAnomaly
from .delay import DelayAnomaly
from .pause import FreezeContainerAnomaly

anomaly_dict = {"loss": PacketLossAnomaly, "delay": DelayAnomaly, "pause": FreezeContainerAnomaly}
