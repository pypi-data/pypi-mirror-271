from requests import Response
from requests.status_codes import codes


class JsonToPythonHook:
    def __init__(self, json_data):
        self.__dict__ = json_data


class ResponseWrapper:
    def __init__(self, response: Response):
        self._response = response

    @property
    def response(self):
        return self._response

    @property
    def body(self):
        return self._response.json(object_hook=JsonToPythonHook)

    def is_array(self) -> bool:
        """
        Check if response body is in array instead of object
        :return: bool
        """
        return type(self.body) == list

    def is_success(self):
        """
        Check if status code is equal to 200
        :return: bool
        """
        return self._response.status_code == codes.okay

    def is_internal_server_error(self):
        """
        Check if status code is equal to 500
        :return: bool
        """
        return self._response.status_code == codes.internal_server_error
