from requests import Response, PreparedRequest
from requests.status_codes import codes


class JsonToPythonHook:
    def __init__(self, json_data):
        self.__dict__ = json_data


class ResponseHandler:
    def __init__(self, response: Response):
        self._resp = response

    @property
    def resp(self) -> Response:
        return self._resp

    @property
    def req(self) -> PreparedRequest:
        return self._resp.request

    @property
    def body(self):
        return self._resp.json(object_hook=JsonToPythonHook)

    @property
    def status_code(self) -> int:
        return self._resp.status_code

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
        return self._resp.status_code == codes.okay

    def is_internal_server_error(self):
        """
        Check if status code is equal to 500
        :return: bool
        """
        return self._resp.status_code == codes.internal_server_error
