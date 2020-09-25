from .base import ConfigParser
from utils import time_to_s
from anomalies import anomaly_dict
from .collector_parsers import LogConfigParser, MetricLogParser
from user_sim import UserSim
from collectors import MetricCollector, LogCollector


class SimulationConfigParser(ConfigParser):
    def __init__(self, config):
        self.duration = self.anomalies = self.user_simulator = self.log_collector = self.metric_collector = None
        super().__init__(config)

    def parse_config(self, config):
        self.duration = time_to_s(config['duration'])
        self.parse_anomalies(config['anomalies'])
        self.parse_user_sim(config['user_sim'])
        self.parse_collectors(config['collectors'])

    def parse_anomalies(self, config):
        self.anomalies = dict()
        for anomaly in config:
            obj = anomaly_dict[anomaly](config[anomaly], name=anomaly)
            obj.timeout = time_to_s(config[anomaly]['timeout'])
            self.anomalies[anomaly] = obj

    def parse_user_sim(self, config):
        name = config['name']
        u_sim_cfg = UserSimConfigParser(config)
        self.user_simulator = UserSim(u_sim_cfg.container_config, u_sim_cfg.user_sim, timeout=u_sim_cfg.timeout,
                                      name=name)

    def parse_collectors(self, config):
        log_parser = LogConfigParser(config['log_collector'])
        self.log_collector = LogCollector(url=log_parser.url, csv_path=log_parser.csv_path)

        metric_parser = MetricLogParser(config['metric_collector'])
        self.metric_collector = MetricCollector(url=metric_parser.url, username=metric_parser.username,
                                                password=metric_parser.password,
                                                csv_path=metric_parser.csv_path,
                                                queries=metric_parser.queries,
                                                duration=metric_parser.duration,
                                                resolution=metric_parser.resolution)


class UserSimConfigParser(ConfigParser):
    class ContainerConfig(ConfigParser):
        def __init__(self, config):
            self.hostname = self.name = None
            super().__init__(config)

        def parse_config(self, config):
            self.hostname = config['hostname']
            self.name = config['name']

    class UserSimConfig(ConfigParser):
        def __init__(self, config):
            self.delay = self.requests = self.clients = self.host = None
            super().__init__(config)

        def parse_config(self, config):
            self.delay = config['delay']
            self.requests = config['requests']
            self.clients = config['clients']
            self.host = config['host']

    def __init__(self, config):
        self.user_sim = self.timeout = self.container_config = None
        super().__init__(config)

    def parse_config(self, config):
        self.user_sim = self.UserSimConfig(config['config']['sim_config'])
        self.container_config = self.ContainerConfig(config['config']['container_config'])
        self.timeout = time_to_s(config['timeout'])
