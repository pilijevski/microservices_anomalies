from time import sleep
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Timer

from utils import time_to_s
from parsers import SimulationConfigParser
from anomalies import anomaly_dict


class Simulation:
    def __init__(self, config):
        if isinstance(config, dict):
            config = SimulationConfigParser(config)
        # assign parsed values
        self.config = config
        self.duration = config.duration
        self.anomalies = config.anomalies
        self.log_collector = config.log_collector
        self.metric_collector = config.metric_collector
        self.user_sim = config.user_simulator

        # executor for running jobs in threads
        self.executor = ThreadPoolExecutor(max_workers=8)
        # here will be stored the anomaly intervals
        self.anomaly_results = dict.fromkeys(list(self.anomalies.keys()), list())

    @staticmethod
    def create_anomalies(anomalies_dict):
        anomalies_o = dict()
        for name, anomaly in anomalies_dict.items():
            anomalies_o[name] = anomaly_dict[name](anomaly['config'], name=name)
            anomalies_o[name].timeout = time_to_s(anomaly['timeout'])
        return anomalies_o

    def run_simulation(self):
        # get the start time of the simulation
        start_time = datetime.utcnow()

        # start simulating user
        self.add_job(self.user_sim, callback_f=self.user_sim_callback)

        # start simulating anomalies
        for a in self.anomalies:
            self.add_job(self.anomalies[a], self.anomaly_callback)

        # run simulation until timeout
        timer = Timer(self.duration, self.end_simulation, {start_time: start_time})
        timer.start()

    def end_simulation(self, start_time):
        # shut down the executor and all running jobs
        self.executor.shutdown(wait=False)
        end_time = datetime.utcnow()
        # store the logs to files
        self.store_logs(start_time, end_time)

    def add_job(self, obj, callback_f):
        try:
            f = self.executor.submit(obj.run)
        except RuntimeError:
            return
        f.add_done_callback(callback_f)

    def anomaly_callback(self, future):
        result = future.result()
        self.anomaly_results[result.name].append((result.start_time, result.end_time))
        sleep(result.timeout)
        self.add_job(result, self.anomaly_callback)

    def user_sim_callback(self, future):
        result = future.result()
        sleep(result.timeout)
        self.add_job(result, self.user_sim_callback)

    def store_logs(self, from_date, to_date):
        self.store_metric_data(from_date, to_date)
        self.store_log_data(from_date, to_date)

    def store_log_data(self, from_date, to_date):
        log_df = self.log_collector.get_data(from_date, to_date)
        log_df = self._create_anomaly_row(log_df)
        self.log_collector.store_data(log_df)

    def store_metric_data(self, from_date, to_date):
        metric_df = self.metric_collector.get_data(from_date, to_date)
        metric_df = self._create_anomaly_row(metric_df)
        self.metric_collector.store_data(metric_df)

    def _create_anomaly_row(self, df):
        for anomaly, timestamps in self.anomaly_results.items():
            df[f"anomaly_{anomaly}"] = 0
            for start_date, end_date in timestamps:
                df.loc[start_date:end_date, f"anomaly_{anomaly}"] = 1
        return df
