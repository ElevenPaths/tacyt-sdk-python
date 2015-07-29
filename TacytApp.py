#!/usr/bin/env python
# -*- coding: utf-8 -*-


from TacytAuth import TacytAuth
from ExternalApiFilterRequest import ExternalApiFilterRequest
from ExternalApiTagRequest import ExternalApiTagRequest
from ExternalApiCompareRequest import ExternalApiCompareRequest
from ExternalApiSearchRequest import ExternalApiSearchRequest
from Filter import Filter

try:
    import simplejson as json
except ImportError:
    import json

json_encode = lambda x: json.dumps(x)
json_decode = lambda x: json.loads(x)


class TacytApp(TacytAuth):

    def __init__(self, app_id, secret_key):
        '''
        Create an instance of the class with the Application ID and secret obtained from Tacyt
        @param $app_id
        @param $secret_key
        '''
        super(TacytApp, self).__init__(app_id, secret_key)


    def search_apps(self, query, numberPage, maxResults):
        result = ExternalApiSearchRequest(query, numberPage, maxResults)
        return self._http("POST", self.API_SEARCH_URL, None, result.get_json_encode())

    def get_app_details(self, key):
        return self._http("GET", self.API_DETAILS_URL + "/" + key)

    def list_tags(self):
        request = ExternalApiTagRequest.enmRequestType.LIST
        result = ExternalApiTagRequest(request, None, None)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict())

    def assign_tag(self, tag, app_keys):
        request = ExternalApiTagRequest.enmRequestType.CREATE
        result = ExternalApiTagRequest(request, tag, app_keys)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict())

    def remove_tag_for_apps(self, tag, app_keys):
        request = ExternalApiTagRequest.enmRequestType.REMOVE
        result = ExternalApiTagRequest(request, tag, app_keys)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict())

    def delete_tag(self, tag):
        request = ExternalApiTagRequest.enmRequestType.REMOVE_ALL
        result = ExternalApiTagRequest(request, tag, None)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict())

    def create_filter(self, filter):
        request = ExternalApiFilterRequest.request_type.CREATE
        result = ExternalApiFilterRequest(request, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict)

    def update_filter(self, filter):
        request = ExternalApiFilterRequest.request_type.UPDATE
        result = ExternalApiFilterRequest(request, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict)

    def read_all_filters(self):
        request = ExternalApiFilterRequest.request_type.READ
        result = ExternalApiFilterRequest(request, None, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict)

    def read_one_filter(self, filter_id):
        request = ExternalApiFilterRequest.request_type.READ
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(request, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict)

    def delete_filter(self, filter_id):
        request = ExternalApiFilterRequest.request_type.DELETE
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(request, filter)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict)

    def search_public_filter(self, query, page):
        request = ExternalApiFilterRequest.request_type.SEARCH_PUBLIC_FILTER
        result = ExternalApiFilterRequest(request, query, page)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_aux)

    def list_detected_apps(self, filter_id, page):
        request = ExternalApiFilterRequest.request_type.LIST_DETECTIONS
        result = ExternalApiFilterRequest(request, filter_id, page)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_aux)

    def un_subscribe_public_filter(self, filter_id):
        request = ExternalApiFilterRequest.request_type.UNSUBSCRIBE
        result = ExternalApiFilterRequest(request, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_aux)

    def subscribe_public_filter(self, filter_id):
        request = ExternalApiFilterRequest.request_type.SUBSCRIBE
        result = ExternalApiFilterRequest(request, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_aux)

    def get_RSS_info(self, filter_id):
        request = ExternalApiFilterRequest.request_type.GET_RSS
        result = ExternalApiFilterRequest(request, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_aux)

    def compare_apps(self, apps, include_details):
        result = ExternalApiCompareRequest(apps, include_details)
        return self._http("POST", self.API_COMPARER_URL, None, result.get_json_encode())
















