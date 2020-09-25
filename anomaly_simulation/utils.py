import json


def time_to_s(time):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(time[:-1]) * seconds_per_unit[time[-1]]


def load_json(json_file):
    with open(json_file, 'rb') as file:
        obj = json.load(file)
    return obj
