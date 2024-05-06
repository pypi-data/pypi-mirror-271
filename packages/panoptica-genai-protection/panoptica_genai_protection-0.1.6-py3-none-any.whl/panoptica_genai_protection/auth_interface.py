class MarvinAuthInterface:
    def get_token(self):
        raise NotImplementedError()

    def init_expired(self):
        raise NotImplementedError()

    def get_headers(self):
        raise NotImplementedError()
