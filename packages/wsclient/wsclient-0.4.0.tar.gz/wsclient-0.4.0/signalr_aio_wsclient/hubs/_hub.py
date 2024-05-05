#!/usr/bin/python
# -*- coding: utf-8 -*-

# signalr_aio/hubs/_hub.py
# Stanislav Lazarov

from fons.log import get_standard_5

logger, logger2, tlogger, tloggers, tlogger0 = get_standard_5(__name__)

_METHODS_WARNED = []


class Hub:
    def __init__(self, name, connection):
        self.name = name
        self.server = HubServer(name, connection, self)
        self.client = HubClient(name, connection)


class HubServer:
    def __init__(self, name, connection, hub):
        self.name = name
        self.__connection = connection
        self.__hub = hub

    def invoke(self, method, *data):
        message = {
            "H": self.name,
            "M": method,
            "A": data,
            "I": self.__connection.increment_send_counter(),
        }
        self.__connection.send(message)


class HubClient(object):
    def __init__(self, name, connection):
        self.name = name
        self.__handlers = {}

        async def handle(**data):
            messages = data["M"] if "M" in data and len(data["M"]) > 0 else {}
            for inner_data in messages:
                hub = inner_data["H"] if "H" in inner_data else ""
                if hub.lower() == self.name.lower():
                    method = inner_data["M"]
                    message = inner_data["A"]
                    if method not in self.__handlers:
                        if method not in _METHODS_WARNED:
                            _METHODS_WARNED.append(method)
                            logger2.error(
                                "SIGNALR RECEIVED NON-REGISTERED METHOD: '{}' (message: '{}')".format(
                                    method, message
                                )
                            )
                    else:
                        await self.__handlers[method](message)

        connection.received += handle

    def on(self, method, handler):
        if method not in self.__handlers:
            self.__handlers[method] = handler

    def off(self, method, handler):
        if method in self.__handlers:
            self.__handlers[method] -= handler
