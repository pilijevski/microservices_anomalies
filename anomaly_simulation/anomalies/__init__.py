from .packet_loss import PacketLossAnomaly
from .delay import DelayAnomaly

anomaly_dict = {"loss": PacketLossAnomaly, "delay": DelayAnomaly}
