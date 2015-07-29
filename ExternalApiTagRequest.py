__author__ = 'ruben.moreno'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''

from tacyt.ExternalApiRequest import ExternalApiRequest

try:
    import simplejson as json

except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)

class ExternalApiTagRequest(ExternalApiRequest):

    FIELD_TAGS = "tags"

    class enmRequestType():
        LIST = "LIST"
        CREATE = "CREATE"
        REMOVE = "REMOVE"
        REMOVE_ALL = "REMOVE_ALL"

    request_type = enmRequestType()
    tag = None
    apps = []

    def enm_request_type(self):
        return self.request_type

    def get_tag(self):
        return self.tag

    def get_apps(self):
        return self.apps

    def __init__(self, request_type, tag, apps):
        self.request_type = request_type
        self.tag = tag
        self.apps = apps

    def get_json_encode_dict(self):
        json_obj = dict()
        if self.request_type is not None:
            json_obj["requestType"] = self.request_type
        if self.tag is not None:
            json_obj["tag"] = self.tag
        if self.apps is not None:
            json_obj["apps"] = self.apps

        return json_obj

    def get_json_encode_string(self):

        return json_encode(self.get_json_encode_dict())



























