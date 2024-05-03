import logging
from abc import abstractmethod

import requests

import responses as bringg_responses


class BringgRequest:
    def __init__(self, url, data):
        self.url = url
        self.data = data
        self.response_class = None
        self._response = None
        self.response = None

    def get_headers(self, token: str = None):
        headers = {
            'Content-Type': 'application/json',
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers

    @abstractmethod
    def set_response_class(self):
        pass

    def serialize_response(self):
        self.response = self.response_class(self._response)

    def post(self):
        try:
            self._response = requests.post(self.url, headers=self.get_headers(), json=self.data)
            self.set_response_class()
            self.serialize_response()
        except Exception as e:
            logging.error(f"Error in post request: {e}")
            raise e
        return self.response


class AuthorizedBringgRequest(BringgRequest):
    def __init__(self, url, data, token):
        super().__init__(url, data)
        self.token = token

    @abstractmethod
    def set_response_class(self):
        pass

    def get_headers(self, token: str = None):
        return super().get_headers(self.token)


class GetTokenRequest(BringgRequest):
    def __init__(self, url, client_id, secret_key):
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': secret_key,
        }
        super().__init__(url, data)

    def set_response_class(self):
        self.response_class = bringg_responses.GetTokenResponse


class AssignDriverRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.AssignDriverResponse


class StartOrderRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.StartOrderResponse


class UpdateDriverLocationRequest(AuthorizedBringgRequest):

    def set_response_class(self):
        self.response_class = bringg_responses.UpdateDriverLocationResponse


class CheckInRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.CheckInResponse


class CheckOutRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.CheckOutResponse


class CompleteOrderRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.CompleteOrderResponse


class CancelOrderRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.CancelOrderResponse


class UpdateOrderRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.UpdateOrderResponse


class AddPODRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.AddPODResponse


class GetMerchantCredentialsRequest(AuthorizedBringgRequest):
    def set_response_class(self):
        self.response_class = bringg_responses.GetMerchantCredentialsResponse
