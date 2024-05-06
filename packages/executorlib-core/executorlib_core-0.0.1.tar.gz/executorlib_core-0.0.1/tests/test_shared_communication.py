import unittest

import numpy as np
import zmq

from executorlib_core.communication import (
    interface_connect,
    interface_shutdown,
    interface_send,
    interface_receive,
)


def calc(i):
    return np.array(i**2)


class TestZMQ(unittest.TestCase):
    def test_initialize_zmq(self):
        message = "test"
        host = "localhost"

        context_server = zmq.Context()
        socket_server = context_server.socket(zmq.PAIR)
        port = str(socket_server.bind_to_random_port("tcp://*"))
        context_client, socket_client = interface_connect(host=host, port=port)
        interface_send(socket=socket_server, result_dict={"message": message})
        self.assertEqual(interface_receive(socket=socket_client), {"message": message})
        interface_shutdown(socket=socket_client, context=context_client)
        interface_shutdown(socket=socket_server, context=context_server)
