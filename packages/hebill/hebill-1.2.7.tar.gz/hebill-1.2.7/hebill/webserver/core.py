import os
from .handle import Handle
from .handle_info import HandleInfo
from http.server import HTTPServer
from ..sys import Sys


class WebServer:
    def __init__(self,  host: str = '', port: int = 8000, root: str = None, handle: Handle = None):
        self._host = host
        self._port = port
        self._server = None
        self._handle = handle if handle is not None else HandleInfo
        self._root = root if root else os.getcwd()

    @property
    def host(self) -> str: return self._host

    @property
    def port(self) -> int: return self._port

    @property
    def handle(self) -> Handle: return self._handle

    @property
    def server(self) -> HTTPServer:
        if self._server is None:
            self._server = HTTPServer((self.host, self.port), self.handle)
        return self._server

    def start(self):
        print(f'Hebill: Server started and listing on:')
        if self.host:
            print(f'- http://{self.host}:{self.port}')
        else:
            print(f'- http://127.0.0.1:{self.port}')
            print(f'- http://localhost:{self.port}')
            for ip in Sys.local_ips():
                if ip != '' and ip is not None and '::' not in ip:
                    print(f'- http://{ip}:{self.port}')

        try:
            self.server.serve_forever()

        except KeyboardInterrupt:
            print(f'Hebill: Server stopped by keyboard interrupt.')
            pass

    def stop(self):
        self.server.server_close()
        print(f'Hebill: Server stopped.')
