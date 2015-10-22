#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015 Eleven Paths
'''
import filter

try:
    import simplejson as json

except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)


class ExternalApiFilterRequest:

    JSON_FIELD_OPERATION = "operation"
    JSON_FIELD_DETECTIONS = "detections"

    FIELD_FILTER = "filter"
    FIELD_FILTERS = "filters"
    FIELD_ID = "id"
    FIELD_TOTAL_COUNT = "totalCount"
    FIELD_LINK = "link"
    FIELD_USER = "user"
    FIELD_PASS = "pass"
    FILTER_MAX_SIZE = 8000
    ERROR_LIMIT_EXCEEDED = "Your filter definition exceeds the size limit of 8000 characters. Please, shorten the description or split the rules in multiple filters."

    CREATE_REQUEST = "CREATE"
    READ_REQUEST = "READ"
    UPDATE_REQUEST = "UPDATE"
    DELETE_REQUEST = "DELETE"
    SEARCH_PUBLIC_FILTER_REQUEST = "SEARCH_PUBLIC_FILTER"
    SUBSCRIBE_REQUEST = "SUBSCRIBE"
    UNSUBSCRIBE_REQUEST = "UNSUBSCRIBE"
    GET_RSS_REQUEST = "GET_RSS"
    LIST_DETECTIONS_REQUEST = "LIST_DETECTIONS"

    request_type = None
    filter = None
    page = None
    content = None

    def __init__(self, request_type=None, filter=None, page=None, content=None):
        self.request_type = request_type
        self.content = content

        if page < 1:
            self.page = 1
        else:
            self.page = page

        self.filter = filter

    def get_json_encode_for_filter_based_requests(self):
        json_obj = dict()

        if self.request_type is not None:
            json_obj = {"requestType": self.request_type}

        if self.filter is not None:

            json_obj["filter"]= {"id": self.filter.id,
                                "name": self.filter.name,
                                "description": self.filter.description,
                                "weight": self.filter.weight,
                                "visibility": self.filter.visibility,
                                "rules": self.filter.rules}

            filter_rules = list()

            if self.filter.rules is not None:
                for rule in self.filter.rules:
                    filter_rules.append({"weight": rule.weight, "content": rule.content})

                json_obj["filter"]["rules"] = filter_rules


        if(len(json.dumps(json_obj))) > self.FILTER_MAX_SIZE:
            raise Exception(self.ERROR_LIMIT_EXCEEDED)
        else :
            return json_obj



    def get_json_encode_dict_filter_for_content_based_requests(self):
        json_obj = dict()

        if self.request_type is not None:
            json_obj["requestType"] = self.request_type

        if self.content is not None:
            json_obj["content"] = self.content

        if self.page is not None:
            json_obj["page"] = self.page


        if(len(json.dumps(json_obj))) > self.FILTER_MAX_SIZE:
            raise Exception(self.ERROR_LIMIT_EXCEEDED)
        else :
            return json_obj

    def get_json_encode_string(self):

        return json_encode(self.get_json_encode_for_filter_based_requests)
