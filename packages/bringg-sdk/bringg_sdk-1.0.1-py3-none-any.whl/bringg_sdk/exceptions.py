class BringgException(Exception):
    pass


class InvalidTokenException(BringgException):
    pass


class InvalidPayloadException(BringgException):
    pass


class OrderNotFoundException(BringgException):
    pass


class GeneralErrorException(BringgException):
    pass


class MissingFieldException(BringgException):
    pass


class TaskAlreadyDoneException(BringgException):
    pass
