class RequestFailed(Exception):
    def __init__(self, message, response):
        Exception.__init__(self, message)
        self.response = response