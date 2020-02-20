"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015-2020 Eleven Paths
"""
try:
    import simplejson as json
except ImportError:
    import json


class TagRequest(object):
    LIST_REQUEST = "LIST"
    CREATE_REQUEST = "CREATE"
    REMOVE_REQUEST = "REMOVE"
    REMOVE_ALL_REQUEST = "REMOVE_ALL"

    def __init__(self, request_type=None, tag=None, apps=None):
        self.request_type = request_type
        self.tag = tag.strip().lower()
        self.apps = apps if apps else []

    def as_dict(self):
        json_obj = dict()
        if self.request_type:
            json_obj["requestType"] = self.request_type
        if self.tag:
            json_obj["tag"] = self.tag
        if self.apps:
            json_obj["apps"] = self.apps
        return json_obj

    def get_json_encode_string(self):
        return json.dumps(self.as_dict())
