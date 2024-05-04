class Client(dict):
    def __init__(self, sid):
        super().__init__()
        self['sid'] = sid

    def sid(self): return self['sid']

