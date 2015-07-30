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
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiSearchRequest(query, numberPage, maxResults)
        return self._http("POST", self.API_SEARCH_URL, None, result.get_json_encode_for_search())

    def get_app_details(self, key):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        return self._http("GET", self.API_DETAILS_URL + "/" + key)

    def list_tags(self):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.LIST_REQUEST, None, None)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict_for_tag_based_requests())

    def assign_tag(self, tag, app_keys):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.CREATE_REQUEST, tag, app_keys)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict_for_tag_based_requests())

    def remove_tag_for_apps(self, tag, app_keys):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.REMOVE_REQUEST, tag, app_keys)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict_for_tag_based_requests())

    def delete_tag(self, tag):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiTagRequest(ExternalApiTagRequest.REMOVE_ALL_REQUEST, tag, None)
        return self._http("POST", self.API_TAGS_URL, None, result.get_json_encode_dict_for_tag_based_requests())

    def create_filter(self, filter):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.CREATE_REQUEST, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_for_filter_based_requests())

    def update_filter(self, filter):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.UPDATE_REQUEST, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_for_filter_based_requests())

    def read_all_filters(self):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.READ_REQUEST, None, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_for_filter_based_requests())

    def read_one_filter(self, filter_id):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.READ_REQUEST, filter, None)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_for_filter_based_requests())

    def delete_filter(self, filter_id):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        filter = Filter(filter_id)
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.DELETE_REQUEST, filter)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_for_filter_based_requests())

    def search_public_filter(self, query, page):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.SEARCH_PUBLIC_FILTER_REQUEST, query, page)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_filter_for_content_based_requests())

    def list_detected_apps(self, filter_id, page):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.LIST_DETECTIONS_REQUEST, filter_id, page)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_filter_for_content_based_requests())

    def un_subscribe_public_filter(self, filter_id):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.UNSUBSCRIBE_REQUEST, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_filter_for_content_based_requests())

    def subscribe_public_filter(self, filter_id):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.SUBSCRIBE_REQUEST, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_filter_for_content_based_requests())

    def get_RSS_info(self, filter_id):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiFilterRequest(ExternalApiFilterRequest.GET_RSS_REQUEST, filter_id)
        return self._http("POST", self.API_FILTERS_URL, None, result.get_json_encode_dict_filter_for_content_based_requests())

    def compare_apps(self, apps, include_details):
        '''
+        The custom header consists of three parts, the method, the appId and the signature.
+        This method returns the specified part if it exists.
+        @param $part The zero indexed part to be returned
+        @param $header The HTTP header value from which to extract the part
+        @return string the specified part from the header or an empty string if not existent
+        '''
        result = ExternalApiCompareRequest(apps, include_details)
        return self._http("POST", self.API_COMPARER_URL, None, result.get_json_encode_for_compare_apps())
