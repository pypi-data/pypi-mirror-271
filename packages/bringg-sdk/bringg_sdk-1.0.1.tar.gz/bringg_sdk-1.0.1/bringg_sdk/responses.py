from abc import abstractmethod
from datetime import datetime

import exceptions as bringg_exceptions
from models import Task


class BringgResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = self.get_status_code()
        self.json = self.get_json()

    def get_status_code(self):
        return self.response.status_code

    def is_success(self):
        return self.status_code == 200

    def validate_response(self):
        if self.status_code == 401:
            raise bringg_exceptions.InvalidTokenException("Invalid token or invalid client_id or secret_key")
        if self.status_code == 403:
            raise bringg_exceptions.InvalidPayloadException("Invalid Payload")

    def get_json(self):
        return self.response.json()


class GetTokenResponse:
    """
    This class is used to parse the response from the get_token request
    """

    def __init__(self, response):
        """
        :param response: it is the response object from the request
        """
        self.response = response
        self.access_token = self.get_token()
        self.token_type = self.get_token_type()
        self.expires_in = self.get_expires_in()
        self.created_at = self.get_created_at()
        self.expire_datetime = self.get_expire_datetime()

    def get_value(self, key):
        return self.response.json().get(key)

    def get_token(self):
        """
        :return: token
        """
        return self.get_value('access_token')

    def get_token_type(self):
        """
        :return: token type mostly  - 'Bearer'
        """
        return self.get_value('token_type')

    def get_expires_in(self):
        """
        :return: The time in seconds when the token expires.
        """
        return self.get_value('expires_in')

    def get_created_at(self):
        """
        :return: The timestamp when the token was created.
        """
        return self.get_value('created_at')

    def get_expire_datetime(self):
        """
        :return: The datetime when the token expires.
        """
        return datetime.fromtimestamp((self.created_at + self.expires_in) / 1e3)


class BringgResponseWithSuccessParameter(BringgResponse):

    def __init__(self, response):
        """
        :param response: it is the response object from the request
        """
        super().__init__(response)
        self.task = None
        if self.is_success():
            self.success_action()
        else:
            self.error_action()

    def is_success(self):
        return self.status_code == 200 and self.json.get('success')

    def get_error(self):
        return self.json.get('message')

    @abstractmethod
    def success_action(self):
        pass

    @abstractmethod
    def error_action(self):
        pass


class BringgResponseWithSuccessAndTask(BringgResponseWithSuccessParameter):
    def success_action(self):
        self.task = Task(self.json.get('task'))

    def error_action(self):
        pass


class AssignDriverResponse(BringgResponseWithSuccessAndTask):
    """
    This class is used to parse the response from the assign_driver request
    """

    def error_action(self):
        error = self.get_error()
        match error:
            case "general error":
                raise bringg_exceptions.GeneralErrorException(error)
            case "Task not found":
                raise bringg_exceptions.OrderNotFoundException(error)
            case _:
                raise Exception(error)


class StartOrderResponse(BringgResponseWithSuccessAndTask):
    """
    This class is used to parse the response from the start_order request
    """

    def error_action(self):
        pass


class UpdateDriverLocationResponse(BringgResponseWithSuccessAndTask):

    def error_action(self):
        error = self.get_error()
        match error:
            case "Missing user id/external_id":
                raise bringg_exceptions.MissingFieldException(error)
            case _:
                raise bringg_exceptions.GeneralErrorException(error)


class CheckInResponse(BringgResponseWithSuccessAndTask):

    def error_action(self):
        error = self.get_error()
        match error:
            case "Can not checkin of a done task":
                raise bringg_exceptions.TaskAlreadyDoneException(error)
            case _:
                raise bringg_exceptions.GeneralErrorException(error)


class CheckOutResponse(BringgResponseWithSuccessAndTask):

    def error_action(self):
        pass


class AddPODResponse(BringgResponseWithSuccessAndTask):
    def success_action(self):
        raise NotImplementedError()

    def error_action(self):
        raise NotImplementedError()


class CompleteOrderResponse(BringgResponseWithSuccessAndTask):
    def success_action(self):
        pass

    def error_action(self):
        pass


class CancelOrderResponse(BringgResponseWithSuccessAndTask):

    def error_action(self):
        pass


class UpdateOrderResponse(BringgResponseWithSuccessParameter):
    def success_action(self):
        raise NotImplementedError()

    def error_action(self):
        raise NotImplementedError()


class GetMerchantCredentialsResponse(BringgResponse):
    def success_action(self):
        raise NotImplementedError()

    def error_action(self):
        raise NotImplementedError()
