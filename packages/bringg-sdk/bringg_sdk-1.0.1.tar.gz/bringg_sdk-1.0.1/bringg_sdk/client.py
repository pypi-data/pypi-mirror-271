from datetime import datetime

import request_factory as bringg_requests
from request_factory import GetTokenRequest, AssignDriverRequest


class BringgClient:
    """
    BringgClient is a client for the Bringg API.
    Documentation: https://developers.bringg.com/reference/api-calls
    Fleet Portal: https://fleet.bringg.com/
    """

    def __init__(self, client_id: str, secret_key: str, environment='production', admin_client_id=None,
                 admin_client_secret=None):
        self.expire_datetime = None
        self.client_id = client_id
        self.secret_key = secret_key
        self.environment = environment
        self.token_expiry = None
        self.token = None
        self.base_url = {
            'production': 'https://us3-admin-api.bringg.com',
            'sandbox': 'https://sandbox-admin-api.bringg.com',
        }
        self.urls = {
            "get_token": "/oauth/token",
            "assign_driver": "/open_fleet_services/assign_driver",
            "update_order": "/open_fleet_services/update_task",
            "update_task": "/open_fleet_services/update_task",
            "cluster_check_in": "/open_fleet_services/cluster_check_in",
            "cluster_check_out": "/open_fleet_services/cluster_check_out",
            "start_order": "/open_fleet_services/start_task",
            "complete_order": "/open_fleet_services/complete_task",
            "update_driver_location": "/open_fleet_services/update_driver_location",
            "check_in": "/open_fleet_services/checkin",
            "checkout": "/open_fleet_services/checkout",
            "add_note": "/open_fleet_services/create_note",
            "cancel_order": "/open_fleet_services/cancel_delivery",
        }
        self.admin_client_id = admin_client_id
        self.admin_client_secret = admin_client_secret

    def get_url(self, url_name: str):
        return self.base_url[self.environment] + self.urls.get(url_name)

    def _get_token(self):
        url = self.get_url('get_token', )
        response = GetTokenRequest(url, self.client_id, self.secret_key).response
        self.token = response.access_token
        self.token_expiry = response.expire_datetime
        return self.token

    def token_is_expired(self):
        return self.token_expiry <= datetime.now()

    def get_token(self):
        if self.token_is_expired():
            return self._get_token()
        return self.token

    def assign_driver(self, task_id: int, driver_external_id: str, driver_name: str, delivery_cost_in_cents=0,
                      green_delivery=True, job_description=None, driver_phone=None, driver_email=None):
        url = self.get_url('assign_driver')
        data = {
            "task_id": task_id,
        }
        if driver_name:
            user = {
                "name": driver_name,
                "external_id": driver_external_id,
                "job_description": job_description,
                "phone": driver_phone,
                "email": driver_email
            }
            data['user'] = user
        else:
            data['external_id'] = driver_external_id
        if delivery_cost_in_cents:
            data['delivery_cost'] = delivery_cost_in_cents
        if green_delivery:
            data['green_delivery'] = green_delivery
        request = AssignDriverRequest(url, data, self.get_token())
        response = request.post()
        return response

    def start_order(self, task_id: int, lat: float | None = None, lng: float | None = None,
                    reported_time_in_timestamp: int = None, delivery_cost_in_cents: int = None, green_delivery=True):
        """
        This endpoint is used to start an order. This is the first step in the delivery process.
        :param task_id:
        :param lat:
        :param lng:
        :param reported_time_in_timestamp:
        :param delivery_cost_in_cents:
        :param green_delivery:
        :return:
        """
        url = self.get_url('start_order')

        data = {
            "task_id": task_id,
            "green_delivery": green_delivery
        }
        if lat and lng:
            data['lat'] = lat
            data['lng'] = lng
        if reported_time_in_timestamp:
            data['reported_time'] = reported_time_in_timestamp
        if delivery_cost_in_cents:
            data['delivery_cost'] = delivery_cost_in_cents

        request = AssignDriverRequest(url, data, self.get_token())
        response = request.post()
        return response

    def update_driver_location(self, user_external_id: str, lat: float, lng: float,
                               reported_time_in_timestamp: int = None, started_tasks: list = None):
        """
        This endpoint is used to update the driver's location.
        :param user_external_id:
        :param lat:
        :param lng:
        :param reported_time_in_timestamp:
        :param started_tasks:
        :return:
        """
        url = self.get_url('update_driver_location')
        data = {
            "external_id": user_external_id,
            "lat": lat,
            "lng": lng
        }
        if reported_time_in_timestamp:
            data['reported_time'] = reported_time_in_timestamp
        if started_tasks:
            data['started_tasks'] = started_tasks
        request = bringg_requests.UpdateDriverLocationRequest(url, data, self.get_token())
        response = request.post()
        return response

    def check_in(self, task_id: int, lat: float, lng: float, reported_time_in_timestamp: int = None,
                 pickup_dropoff_option: str = None):
        """
        This endpoint is used to check in the driver to the pickup or drop-off location.
        :param task_id: bringg order id
        :param lat: driver latitude
        :param lng: driver longitude
        :param reported_time_in_timestamp:
        :param pickup_dropoff_option: choices: ['pickup', 'dropoff']
        :return:
        """
        if pickup_dropoff_option not in ['pickup', 'dropoff']:
            raise ValueError("pickup_dropoff_option should be either 'pickup' or 'dropoff'")
        url = self.get_url('check_in')
        data = {
            "task_id": task_id,
            "lat": lat,
            "lng": lng,
            "reported_time": reported_time_in_timestamp,
            "pickup_dropoff_option": pickup_dropoff_option
        }
        request = bringg_requests.CheckInRequest(url, data, self.get_token())
        response = request.post()
        return response

    def check_out(self, task_id: int, lat: float, lng: float, reported_time_in_timestamp: int = None,
                  pickup_dropoff_option: str = None):
        """
        :param task_id: bringg order id
        :param lat: driver latitude
        :param lng: driver longitude
        :param reported_time_in_timestamp:
        :param pickup_dropoff_option: choices: ['pickup', 'dropoff']
        :return:
        """
        if pickup_dropoff_option not in ['pickup', 'dropoff']:
            raise ValueError("pickup_dropoff_option should be either 'pickup' or 'dropoff'")
        url = self.get_url('check_in')
        data = {
            "task_id": task_id,
            "lat": lat,
            "lng": lng,
            "reported_time": reported_time_in_timestamp,
            "pickup_dropoff_option": pickup_dropoff_option
        }

        request = bringg_requests.CheckOutRequest(url, data, self.get_token())
        response = request.post()
        return response

    def add_pod(self, note_type: str, task_id: int, lat: float, lng: float, reported_time_in_timestamp: int = None, ):
        """

        :param note_type: choices: TaskNote
        :param task_id:
        :param lat:
        :param lng:
        :param reported_time_in_timestamp:
        :return:
        """

        raise NotImplementedError()

    def complete_order(self, task_id: int, lat: float = None, lng: float = None, reported_time_in_timestamp: int = None,
                       delivery_cost_in_cents: int = None):
        """
        This endpoint is used to complete an order. This is the last step in the delivery process.
        :param task_id:
        :param lat:
        :param lng:
        :param reported_time_in_timestamp:
        :param delivery_cost_in_cents:
        :return:
        """
        url = self.get_url('complete_order')
        data = {
            "task_id": task_id
        }
        if lat and lng:
            data['lat'] = lat
            data['lng'] = lng
        if reported_time_in_timestamp:
            data['reported_time'] = reported_time_in_timestamp
        if delivery_cost_in_cents:
            data['delivery_cost'] = delivery_cost_in_cents
        request = bringg_requests.CompleteOrderRequest(url, data, self.get_token())
        response = request.post()
        return response

    def cancel_order(self, task_id: int, reason_id: int = 0, reason: str = None, lng: float = None,
                     lat: float = None, reported_time_in_timestamp: int = None):
        """
        This endpoint is used to cancel an order.
        :param task_id: Bringg's unique ID for this order. Use either this field or task_external_id to identify the
                        relevant order.
        :param reason_id: MANDATORY: Bringg's reason ID for this order
                                     You will usually get this value from discussions with the relevant merchant
                                     As a default, use 0
        :param reason: The reason you are cancelling the order/delivery
        :param lng: The latitude of where the driver was when the order was started
        :param lat: The latitude of where the driver was when the order was started
        :param reported_time_in_timestamp: The time in milliseconds when the order was started
        :return:
        """
        url = self.get_url('cancel_order')
        data = {
            "task_id": task_id,
            "reason_id": reason_id
        }
        if reason:
            data['reason'] = reason
        if lng and lat:
            data['lng'] = lng
            data['lat'] = lat
        if reported_time_in_timestamp:
            data['reported_time'] = reported_time_in_timestamp
        request = bringg_requests.CancelOrderRequest(url, data, self.get_token())
        response = request.post()
        return response

    def update_order(self):

        raise NotImplementedError()

    def get_merchant_credentials(self):
        """
        Call this endpoint to get the endpoints as well as the Client ID and Client Secret for all merchants that have added your fleet.
        This endpoint can be found under the "Registration Merchants" section.
        Note: After "open_fleet_administration" in the URL is your fleet UUID.
        To get credentials for a specific merchant only, add the merchant_uuid to the end of the URL
        e.g. /open_fleet_administration/<your_fleet_uuid>/<merchant_uuid>

        Authentication:
        To call this endpoint, you will need to use Basic Auth authentication.
        Click the blue "Show Credentials" button under "Admin Credentials" to reveal the Client ID and Client Secret.
        For the Username, use Client ID. For the Password, use Client Secret.
        :return:
        """
        raise NotImplementedError()
