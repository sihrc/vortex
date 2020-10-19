class VortexException(Exception):
    def __init__(self, message, code=400, **kwargs):
        self.code = code
        self.message = message
        self.body = kwargs
        super().__init__("{}. status={}".format(message, code))

    def to_dict(self):
        return {"message": self.message, "code": self.code, "body": self.body}


class UnhandledException(VortexException):
    def __init__(self):
        super().__init__("Internal Server Error", code=500)
