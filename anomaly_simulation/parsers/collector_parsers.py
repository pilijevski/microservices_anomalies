from .base import ConfigParser


class LogConfigParser(ConfigParser):
    def __init__(self, config):
        self.csv_path = self.url = None
        super().__init__(config)

    def parse_config(self, config):
        self.url = config['target_url']
        self.csv_path = config['csv_path']


class MetricLogParser(ConfigParser):
    def __init__(self, config):
        self.url = self.username = self.password = self.csv_path = None
        self.queries = self.duration = self.resolution = None
        super().__init__(config)

    def parse_config(self, config):
        self.url = config['url']
        self.duration = config['duration']
        self.resolution = config['resolution']

        self.queries = config['queries']
        self.username = config['username']
        self.password = config['password']
        self.csv_path = config['csv_path']
