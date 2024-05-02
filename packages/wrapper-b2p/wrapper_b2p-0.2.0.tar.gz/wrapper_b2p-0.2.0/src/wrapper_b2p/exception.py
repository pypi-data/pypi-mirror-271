class BaseExceptionB2P(Exception):
    pass


class ErrorConnectB2P(BaseExceptionB2P):
    def __init__(self, message='B2P service not responding, please try again later'):
        self.message = message
        super().__init__(self.message)


class ErrorPayerIDNotExist(BaseExceptionB2P):
    def __init__(self, message="You must specify the payer's ID"):
        self.message = message
        super().__init__(self.message)


class ErrorDefined(BaseExceptionB2P):
    def __init__(self, message="ID or Reference defined"):
        self.message = message
        super().__init__(self.message)
