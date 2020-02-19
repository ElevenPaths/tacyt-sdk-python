"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""

import json

from deprecated import deprecated

from tacyt_sdk.authorization.error import Error
from tacyt_sdk.version import Version


class Response(object):
    """This class models a response from any of the endpoints in the Tacyt API.
    It consists of a "data" and an "error" elements. Although normally only one
    of them will be present, they are not mutually exclusive, since errors can
    be non fatal, and therefore a response could have valid information
    in the data field and at the same time inform of an error.
    """
    def __init__(self, json_string=None):
        try:
            content = json.loads(json_string)
        except ValueError:
            content = {}

        self.data = content.get("data", "")
        self.error = ""
        if "error" in content:
            self.error = Error(content["error"])

    @deprecated(version=Version.API_VERSION,
                reason="You should use directly the attribute")
    def get_error(self):
        return self.error

    @deprecated(version=Version.API_VERSION,
                reason="You should use directly the attribute")
    def get_data(self):
        return self.data

    def as_dict(self):
        """Return the response as a dict.
        :return The data and error parsed from the response
        :rtype dict
        """
        response_data = dict()
        if self.data:
            response_data["data"] = self.data
        if self.error:
            response_data["error"] = self.error
        return response_data
