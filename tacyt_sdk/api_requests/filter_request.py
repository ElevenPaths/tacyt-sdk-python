"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""
try:
    import simplejson as json
except ImportError:
    import json


class FilterRequest(object):
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
    ERROR_LIMIT_EXCEEDED = ("Your filter definition exceeds the size limit "
                            "of {} characters. Please, shorten the "
                            "description or split the rules in "
                            "multiple filters.".format(FILTER_MAX_SIZE))
    CREATE_REQUEST = "CREATE"
    READ_REQUEST = "READ"
    UPDATE_REQUEST = "UPDATE"
    DELETE_REQUEST = "DELETE"
    SEARCH_PUBLIC_FILTER_REQUEST = "SEARCH_PUBLIC_FILTER"
    SUBSCRIBE_REQUEST = "SUBSCRIBE"
    UNSUBSCRIBE_REQUEST = "UNSUBSCRIBE"
    GET_RSS_REQUEST = "GET_RSS"
    LIST_DETECTIONS_REQUEST = "LIST_DETECTIONS"
    READ_GROUPS = "READ_GROUPS"
    LIST_GROUP_DETECTIONS = "LIST_GROUP_DETECTIONS"
    GET_GROUP_RSS = "GET_GROUP_RSS"

    def __init__(self, request_type=None, filter_object=None, page=None,
                 content=None):
        self.request_type = request_type
        self.content = content
        self.page = page if page else 1
        self.filter_object = filter_object

    def as_dict(self):
        data = dict()

        if self.request_type:
            data["requestType"] = self.request_type

        if self.filter_object:
            data["filter"] = self.filter_object.as_dict()

        if self.page:
            data["page"] = self.page

        if self.content:
            data["content"] = self.content

        if len(json.dumps(data)) > self.FILTER_MAX_SIZE:
            raise ValueError(self.ERROR_LIMIT_EXCEEDED)
        return data

    def get_json_encode_string(self):
        return json.dumps(self.as_dict)
