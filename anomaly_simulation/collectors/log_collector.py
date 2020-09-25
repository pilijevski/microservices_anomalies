import json
import collections.abc
import pandas as pd
import requests
import time
import os
from requests.auth import HTTPBasicAuth


class LogCollector:
    def __init__(self, url, csv_path):
        path = os.path.join(os.path.dirname(__file__), "../config", "log_collector.json")
        self.query = json.load(open(path, 'rb'))
        self.from_date = "2020-09-11T00:00:00.000"
        self.to_date = "2020-09-11T00:00:00.000"
        self.csv_path = csv_path
        self.url = url

    def set_start_date(self, from_date):
        self.from_date = from_date
        self.update_query()

    def set_end_date(self, to_date):
        self.to_date = to_date
        self.update_query()

    def set_dates(self, from_date, to_date):
        self.to_date = to_date
        self.from_date = from_date
        self.update_query()

    def update_query(self):
        self.query["query"]["constant_score"]["filter"]["range"]["@timestamp"]["from"] = pd.to_datetime(
            self.from_date).isoformat()
        self.query["query"]["constant_score"]["filter"]["range"]["@timestamp"]["to"] = pd.to_datetime(
            self.to_date).isoformat()

    def construct_exec_string(self):
        return f"es2csv -q es2csv -u {self.url}" \
               f" -e -f _all -r -q '{json.dumps(self.query)}' -o {self.csv_path} --debug"

    def get_data(self, from_date, to_date):
        self.set_dates(from_date, to_date)
        exec_str = self.construct_exec_string()
        os.system(exec_str)
        df = pd.read_csv(self.csv_path, index_col='@timestamp')
        df.index = pd.to_datetime(df.index, infer_datetime_format=True).tz_localize(None)
        df = df.sort_index()
        return df

    def store_data(self, df):
        df.to_csv(self.csv_path)


class MetricCollector:
    def __init__(self, url, username, password, csv_path, queries=None, duration='1m', resolution='1m'):
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(username, password)
        self.url = url
        self.csv_path = csv_path
        self.duration = duration
        self.resolution = resolution
        self.queries = queries or dict()

    def get_matrix_names(self, url):
        new_url = '{0}/api/v1/label/__name__/values'.format(url)
        response = requests.get(new_url, auth=self.auth)
        names = response.json()['data']
        return names

    def get_data(self, from_date, to_date):
        if len(self.queries) == 0:
            return self.get_raw_data(from_date, to_date)

        df = pd.DataFrame()
        for name, query in self.queries.items():
            query = f"({query})[{self.duration}:{self.resolution}]"
            response = requests.get(f'{self.url}/api/v1/query', params={'query': query},
                                    auth=self.auth)
            results = response.json()['data']['result']
            results = [self.correct_values(self.flatten(result), name) for result in results]
            if len(results) > 0:
                df = df.append(pd.DataFrame(index=list(results[0].keys()), data=results[0].values()).T)

        df = df.set_index('timestamp')
        df.index = pd.to_datetime(pd.Series(df.index))
        df = df.sort_index()
        return df

    def get_raw_data(self, from_date=None, to_date=None):
        matrix_names = self.get_matrix_names(self.url)
        df = pd.DataFrame()
        for matrix_name in matrix_names:
            response = requests.get(f'{self.url}/api/v1/query', params={'query': matrix_name + '[1s]'},
                                    auth=self.auth)
            results = response.json()['data']['result']
            results = [self.correct_values(self.flatten(result)) for result in results]
            df = df.append(pd.DataFrame().from_records(results))
        df = df.set_index('timestamp')
        df.index = pd.to_datetime(pd.Series(df.index))
        df = df.sort_index()
        return df[from_date:to_date]

    def store_data(self, df):
        df.to_csv(self.csv_path)

    def flatten(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def correct_values(d, name='value'):
        new_d = dict()
        val = 'value' if 'value' in d.keys() else 'values'
        if not isinstance(d[val][0], list):
            d[val][0] = [d[val][0]]
        ms = [_get_ms(d[val][i][0]) for i in range(len(d[val]))]
        new_d['timestamp'] = [time.strftime('%Y-%m-%d %H:%M:%S.{}'.format(ms[i]), time.gmtime(d[val][i][0]))
                              for i in range(len(d[val]))]
        new_d[name] = [d[val][i][1] for i in range(len(d[val]))]
        del d[val]
        new_d['labels'] = d
        return new_d


def _get_ms(val):
    parts = repr(val).split('.')
    if len(parts) > 1:
        return parts[1]
    return parts[0]
