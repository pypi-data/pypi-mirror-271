from .gets.core import Gets
from .posts.core import Posts
from .cookies.core import Cookies
from .headers.core import Headers


class Request(dict):
    def __init__(self, cookie: dict = None, get: dict = None, post: dict = None, headers: dict = None):
        super().__init__()
        self['cookies'] = Cookies(cookie)
        self['gets'] = Gets(get)
        self['posts'] = Posts(post)
        self['headers'] = Headers(headers)

    @property
    def cookies(self) -> Cookies: return self['cookies']

    @property
    def gets(self) -> Gets: return self['gets']

    @property
    def posts(self) -> Posts: return self['posts']

    @property
    def headers(self) -> Headers: return self['headers']
