#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015 Eleven Paths
'''
from tacyt.ExternalApiRequest import ExternalApiRequest
from tacyt.Filter import Filter

try:
    import simplejson as json

except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)


class ExternalApiFilterRequest(ExternalApiRequest):
    JSON_FIELD_OPERATION = "operation"
    JSON_FIELD_DETECTIONS = "detections"

    FIELD_FILTER = "filter"
    FIELD_FILTERS = "filters"
    FIELD_ID = "id"
    FIELD_TOTAL_COUNT = "totalCount"
    FIELD_LINK = "link"
    FIELD_USER = "user"
    FIELD_PASS = "pass"

    class RequestType():

        CREATE = "CREATE"
        READ = "READ"
        UPDATE = "UPDATE"
        DELETE = "DELETE"
        SEARCH_PUBLIC_FILTER = "SEARCH_PUBLIC_FILTER"
        SUBSCRIBE = "SUBSCRIBE"
        UNSUBSCRIBE = "UNSUBSCRIBE"
        GET_RSS = "GET_RSS"
        LIST_DETECTIONS = "LIST_DETECTIONS"

    request_type = RequestType()
    filter = None
    content = None
    page = None

    def __init__(self, request_type=None, content=None, page=None):
        self.request_type = request_type
        self.content = content
        self.page = page


    @property
    def get_json_encode_dict(self):
        json_obj = dict()

        if self.request_type is not None:
            json_obj = {"requestType": self.request_type}

        if self.content is not None:

            json_obj["filter"]= {"id": self.content.id,
                                "name": self.content.name,
                                "description": self.content.description,
                                "weight": self.content.weight,
                                "visibility": self.content.visibility,
                                "rules": self.content.rules}

            content_rules = list()

            if self.content.rules is not None:
                for i in self.content.rules:
                    content_rules.append({"weight": i.weight, "content": i.content})

                json_obj["filter"]["rules"] = content_rules

        return json_obj


    def get_json_encode_dict_aux(self):
        json_obj = dict()

        if self.request_type is not None:
            json_obj["requestType"] = self.request_type

        if self.content is not None:
            json_obj["content"] = self.content

        if self.page is not None:
            json_obj["page"] = self.page

        return json_obj

    def get_json_encode_string(self):
        return json_encode(self.get_json_encode_dict)
