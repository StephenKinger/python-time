#!/usr/bin/python

"""
The following is an python parser for influxdb client.
the following module requires the following python pkgs {influxdb, concurrent.futures}
"""


from concurrent.futures import ThreadPoolExecutor
from influxdb import client


def get_time_pattern(timestamp):
    return int(str(timestamp).split('.')[0] + str(timestamp).split('.')[1] + '0000000')


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class GetInflux(object):
    def __init__(self, server, port, db, table_name,
                 pattern=None):
        # args
        self.pattern = pattern
        self.server = server
        self.db_name = db
        self.table_name = table_name
        self.port = port

        self.influx_connection = None
        self.get_influx_client()
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.running = True

    def is_running(self):
        return self.running


    def get_influx_client(self):
        self.influx_connection = client.InfluxDBClient(host=self.server, database=self.db_name)
        found = False
        for db_name_entry in self.influx_connection.get_list_database():
            if self.db_name == db_name_entry["name"]:
                found = True
        if found == False:
            self.influx_connection.create_database(self.db_name)

    def send_influx_points(self, points):
        try:
            if self.influx_connection is None:
                self.get_influx_client()
            self.influx_connection.write_points(points)
        except Exception as e:
            print('cannot add data points {0} due to {1}'.format(points, e))

    def send(self, trans_name, timestamp, duration, sent=0, recv=0):
        try:
            json_body = [
                {
                    "measurement": self.table_name,
                    "tags": {
                        "response time": trans_name
                    },
                    "time": get_time_pattern(timestamp),
                    "fields": {
                        "value": duration,
                        "bytes_sent": sent,
                        "bytes_recv": recv
                    }
                }
            ]
            self.executor.submit(self.send_influx_points, json_body)
        except Exception as e:
            print('failed to send data points'.format(e))

    def close(self):
        self.influx_connection.close()