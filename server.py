import atexit
import datetime
import grpc
import hashlib
import multiprocessing
import os
import random
import schedule
import signal
import sys
import time
from concurrent import futures
from logging import getLogger, Formatter, DEBUG
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Process, Manager

import example_pb2
import example_pb2_grpc

_ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT / 2

logger = getLogger()
logger.setLevel(DEBUG)
logging_handler = TimedRotatingFileHandler(filename="app.log", when='H')
logging_format = "[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s (%(threadName)s): %(message)s"
logging_handler.setFormatter(Formatter(logging_format))
logger.addHandler(logging_handler)

Pid = os.getpid()


def signal_handler(signum=None, frame=None):
    """
    :param signum:
    :param frame:
    :return:
    """
    logger.info("Interrupted by the signal. Killing pid {}".format(Pid))
    logger.info("Signal number: {} | {}".format(signum, frame))
    os.kill(Pid, signal.SIGKILL)
    logger.info('killed pid: %d' % (Pid,))
    sys.exit(1)


def _is_same_hash(a, b):
    ha = hashlib.md5(str(a).encode("utf-8")).hexdigest()
    hb = hashlib.md5(str(b).encode("utf-8")).hexdigest()
    return ha == hb


class ExampleServicer(example_pb2_grpc.ExampleServiceServicer):

    def __init__(self, shared_memory):
        self.shared_memory = dict(shared_memory)

    def update_shared_memory(self, shared_memory) -> bool:
        if not _is_same_hash(self.shared_memory, dict(shared_memory)):
            self.shared_memory = dict(shared_memory)
            return True
        return False

    def ExampleServer(self, request: example_pb2.Request, context: grpc.ServicerContext) -> example_pb2.Reply:
        message = request.message
        logger.debug("message: {}".format(message))
        logger.debug(self.shared_memory)
        responses = [
            example_pb2.Reply.Response(key=str(k), value=str(self.shared_memory[k]))
            for k in self.shared_memory
        ]
        logger.debug("response: {}".format(responses))
        return example_pb2.Reply(responses=responses)


def _worker(shared_memory):
    logger.debug("Refresh shared memory")
    value = random.choice(range(10))
    key = hashlib.md5(str(value).encode("utf-8")).hexdigest()
    shared_memory[key] = value
    logger.debug("#_worker$shared_memory: {}".format(shared_memory))


def _run_server(servicer, port):
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=2),
        options=(('grpc.so_reuseport', 1),)
    )
    example_pb2_grpc.add_ExampleServiceServicer_to_server(servicer, grpc_server)
    grpc_server.add_insecure_port("[::]:{}".format(port))
    logger.debug("Start gRPC server...")
    grpc_server.start()
    logger.debug("Started gRPC server.")

    atexit.register(grpc_server.stop, 0)

    _wait_forever(grpc_server)


def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


def main():
    atexit.register(signal_handler)

    ports = [50051, 50052, 50053, 50054]
    with Manager() as manager:

        shared_memory = manager.dict()

        _worker(shared_memory)
        schedule.every(10).seconds.do(_worker, shared_memory)

        servicer = ExampleServicer(shared_memory)
        servers = {}
        for port in ports:
            servers[str(port)] = Process(target=_run_server, args=(servicer, port,))
        for port in servers:
            server = servers[port]
            server.start()

        try:
            while True:
                schedule.run_pending()
                is_updated = servicer.update_shared_memory(shared_memory)
                if is_updated:
                    logger.debug("Updated shared memory")
                    for port in servers:
                        servers[port].terminate()
                    servicer = ExampleServicer(shared_memory)
                    servers = {}
                    for port in ports:
                        servers[str(port)] = Process(target=_run_server, args=(servicer, port,))
                    for port in servers:
                        server = servers[port]
                        server.start()
                time.sleep(1)
        except KeyboardInterrupt:
            for port in servers:
                servers[port].terminate()


if __name__ == "__main__":
    main()
