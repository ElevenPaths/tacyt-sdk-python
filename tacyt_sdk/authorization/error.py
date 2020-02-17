"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""

import json


class Error:
    def __init__(self, error_data):
        self.code = error_data['code']
        self.message = error_data['message']

    def as_dict(self):
        return {"code": self.code, "message": self.message}

    def __repr__(self):
        return json.dumps(self.as_dict())

    def __str__(self):
        return self.__repr__()
