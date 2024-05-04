from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from .features.request.core import Request


class Handle(BaseHTTPRequestHandler):
    def __init__(self, client_address, request, server):
        self._requests = Request()
        super().__init__(client_address, request, server)

    @property
    def requests(self) -> Request:
        return self._requests

    def response(self) -> str:
        return f'Hello World.'

    def do_GET(self):
        # 由于每次连接都会有GET favicon.ico，避免多余的GET处理
        if self.path == '/favicon.ico':
            from ..image import PNGIconHebill
            icon = PNGIconHebill()
            self.send_response(200)
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(icon.bites)
        else:
            # Refer to the reference.txt
            for key, value in dict(self.headers).items():
                self.requests.headers[key] = value

            if 'Cookie' in self.requests.headers:
                for key, morsel in SimpleCookie(self.requests.headers['Cookie']).items():
                    self.requests.cookies[key] = morsel.value
            get_parameters = urlparse(self.path).query
            if get_parameters:
                for p in get_parameters.split('&'):
                    k, v = p.split('=')
                    self.requests.gets[k] = v
            url = self.rfile.read(int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0)
            post_parameters = parse_qs(url.decode('utf-8'))
            for k, v in post_parameters.items():
                self.requests.posts[k] = v
            # 继续相关操作
            try:
                # 发送响应状态码
                self.send_response(200)
                # 设置响应头
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # 响应内容
                self.wfile.write(self.response().encode('utf-8'))  # 将字符串转换为字节流并发送
            except ConnectionAbortedError as e:
                print("Hebill: Connection interrupted by user.", e)

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
