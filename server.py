#!/usr/bin/env python3

import math
import signal
from sys import argv

import Pyro5.api


@Pyro5.api.expose
class Eco(object):
    def __init__(self, max_msgs: int = 3):
        self.count = 0
        self.current_msgs = []
        self.max_msgs = max_msgs

    def voter(self):
        signal.alarm(0)
        received_msgs = self.current_msgs[:]
        self.current_msgs = []
        majority = math.ceil((self.max_msgs + 1) / 2)
        if len(received_msgs) >= majority:
            for msg in received_msgs[:majority]:
                if received_msgs.count(msg) >= majority:
                    return msg
        return "Inconclusive"

    def send(self, message):
        if self.current_message_is_empty():
            return self.message_delivery(message)

        self.current_msgs.append(message)
        if len(self.current_msgs) == self.max_msgs:
            print(self.voter())
        return "Msg delivered"

    def message_delivery(self, message):
        self.current_msgs.append(message)
        self.count += 1
        signal.alarm(10)
        return "Msg delivered"

    def current_message_is_empty(self):
        return not self.current_msgs

    def counter(self):
        return self.count

    def time_out(self, signum, pilha):
        print("timeout")
        print(self.voter())


def get_name_in_args():
    if len(argv) < 2:
        print(f"USO: {argv[0]} <nome>")
        exit(1)
    return argv[1]


def configure_server(ns_name: str):
    eco = Eco(max_msgs=5)  # servant
    uri = daemon.register(eco)  # register pyro obj
    signal.signal(signal.SIGALRM, eco.time_out)
    print("uri:", uri)  # publish url
    ns = Pyro5.api.locate_ns()  # NS
    ns.register(ns_name, uri)  # register ref in ns (name servers)


if __name__ == "__main__":
    name = get_name_in_args()
    daemon = Pyro5.api.Daemon()  # daemon Pyro
    configure_server(name)

    print(f'"{name}" waiting request.')
    daemon.requestLoop()
