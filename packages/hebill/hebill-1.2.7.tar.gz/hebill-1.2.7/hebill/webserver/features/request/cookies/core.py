class Cookies(dict):
    def __init__(self, data: dict = None):
        super().__init__()
        if data is not None:
            self.update(data)

    def sid(self): return self.get('sid', None)

