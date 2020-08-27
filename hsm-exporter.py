import re
import time
import argparse
import os

from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client import start_http_server

mdt_path = '/proc/fs/lustre/mdt/'
# mdt_path = 'test/fs/lustre/mdt/'


class HSMCollector(object):
    def __init__(self):
        pass

    def collect(self):
        gauge_actions = GaugeMetricFamily(
            'hsm_actions', 'Actions in the queue',
            labels=['action', 'archive_id', 'status', 'mdt'])
        gauge_agents = GaugeMetricFamily(
            'hsm_agents', 'Agents consuming from the queue',
            labels=['uuid', 'archive_id', 'mdt', 'status'])
        for mdt in os.listdir(mdt_path):
            with open(mdt_path + mdt + '/hsm/actions', 'r') as actions_f:
                actions = {}
                for action in actions_f.readlines():
                    m = re.search(
                        r'action=(\w+).*archive#=(\d+).*status=(\w+)', action)
                    k = (m.group(1), m.group(2), m.group(3))
                    if k in actions:
                        actions[k] += 1
                    else:
                        actions[k] = 1
                for k in actions.keys():
                    gauge_actions.add_metric([k[0], k[1], k[2], mdt],
                                             actions[k])
            with open(mdt_path + mdt + '/hsm/agents', 'r') as agents_f:
                for agent in agents_f.readlines():
                    m = re.search(r'uuid=(.*) archive_id=(\d+) requests=\[current:(.*) ok:(.*) errors:(.*)\]',  # noqa: E501
                                  agent)
                    gauge_agents.add_metric(
                        [m.group(1), m.group(2), mdt, 'current'], m.group(3))
                    gauge_agents.add_metric(
                        [m.group(1), m.group(2), mdt, 'ok'], m.group(4))
                    gauge_agents.add_metric(
                        [m.group(1), m.group(2), mdt, 'errors'], m.group(5))
        yield gauge_actions
        yield gauge_agents


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Prometheus collector for the hsm stats on Lustre')
    parser.add_argument(
        '--port',
        type=int,
        default=8081,
        help='Collector http port, default is 8081')

    args = parser.parse_args()

    start_http_server(args.port)
    REGISTRY.register(HSMCollector())
    while True:
        time.sleep(1)
