"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015-2020 Eleven Paths
"""

import json


class Error(object):
    def __init__(self, error_data):
        self.code = error_data['code']
        self.message = error_data['message']
        missing_arguments = error_data.get("args", "").split(",")
        self.args = [arg.strip() for arg in missing_arguments if arg]

    def as_dict(self):
        return {"code": self.code, "message": self.message,
                "args": "".join(self.args)}

    def __repr__(self):
        return json.dumps(self.as_dict())

    def __str__(self):
        return self.__repr__()
