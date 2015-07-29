#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TacytResponse import TacytResponse
import logging
import time
import json
import hashlib


class TacytAuth(object):

    API_VERSION = "1.3"
    API_HOST = "path5.11paths.com"
    API_PORT = 443
    API_HTTPS = True
    API_PROXY = None
    API_PROXY_PORT = None
    API_SEARCH_URL = "/api/"+API_VERSION+"/search"
    API_DETAILS_URL = "/api/"+API_VERSION+"/details"
    API_FILTERS_URL = "/api/"+API_VERSION+"/filters"
    API_TAGS_URL = "/api/"+API_VERSION+"/tags"
    API_COMPARER_URL = "/api/"+API_VERSION+"/compare"

    AUTHORIZATION_HEADER_NAME = "Authorization"
    DATE_HEADER_NAME = "X-11Paths-Date"
    AUTHORIZATION_METHOD = "11PATHS"
    X_11PATHS_HEADER_PREFIX = "X-11paths-"
    BODY_HASH_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "Body-Hash"
    AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "

    UTC_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"

    X_11PATHS_HEADER_PREFIX = "X-11paths-"
    X_11PATHS_HEADER_SEPARATOR = ":"

    @staticmethod
    def set_host(host):
        '''
        @param $host The host to be connected with (http://hostname) or (https://hostname)
        '''
        if host.startswith("http://"):

            TacytAuth.API_HOST = host[len("http://"):]
            TacytAuth.API_PORT = 80
            TacytAuth.API_HTTPS = False

        elif host.startswith("https://"):
            TacytAuth.API_HOST = host[len("https://"):]
            TacytAuth.API_PORT = 443
            TacytAuth.API_HTTPS = True

    @staticmethod
    def set_proxy(proxy, port):
        '''
        Enable using a Proxy to connect through
        @param $proxy The proxy server
        @param $port The proxy port number
        '''
        TacytAuth.API_PROXY = proxy
        TacytAuth.API_PROXY_PORT = port

    @staticmethod
    def get_part_from_header(part, header):
        '''
        The custom header consists of three parts, the method, the appId and the signature.
        This method returns the specified part if it exists.
        @param $part The zero indexed part to be returned
        @param $header The HTTP header value from which to extract the part
        @return string the specified part from the header or an empty string if not existent
        '''
        if header:
            parts = header.split(TacytAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR)
            if len(parts) >= part:
                return parts[part]
        return ""

    @staticmethod
    def get_auth_method_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the Authorization method. Typical values are "Basic", "Digest" or "11PATHS"
        '''
        return TacytAuth.get_part_from_header(0, authorization_header)

    @staticmethod
    def get_appId_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the requesting application Id. Identifies the application using the API
        '''
        return TacytAuth.get_part_from_header(1, authorization_header)

    @staticmethod
    def get_signature_from_header(authorization_header):
        '''
        @param $authorization_header Authorization HTTP Header
        @return string the signature of the current request. Verifies the identity of the application using the API
        '''
        return TacytAuth.get_part_from_header(2, authorization_header)

    @staticmethod
    def get_current_UTC():
        '''
        @return a string representation of the current time in UTC to be used in a Date HTTP Header
        '''
        return time.strftime(TacytAuth.UTC_STRING_FORMAT, time.gmtime())

    def __init__(self, appId, secretKey):
        '''
        Create an instance of the class with the Application ID and secret obtained from Tacyt
        @param $appId
        @param $secretKey
        '''
        self.appId = appId
        self.secretKey = secretKey

    def _http(self, method, url, x_headers=None, body=None):
        '''
        HTTP Request to the specified API endpoint
        @param method string
        @param x_headers list
        @param body dict json
        @return TacytResponse
        '''
        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib

        json_body = json.dumps(body)


        if body is None:
            auth_headers = self.authentication_headers(method, url, x_headers, None, None)
        else:
            auth_headers = self.authentication_headers_with_body(method, url, x_headers, json_body, None)

        if TacytAuth.API_PROXY != None:
            if TacytAuth.API_HTTPS:
                conn = http.HTTPSConnection(TacytAuth.API_PROXY, TacytAuth.API_PROXY_PORT)
                conn.set_tunnel(TacytAuth.API_HOST, TacytAuth.API_PORT)
            else:
                conn = http.HTTPConnection(TacytAuth.API_PROXY, TacytAuth.API_PROXY_PORT)
                url = "http://" + TacytAuth.API_HOST + url
        else:
            if TacytAuth.API_HTTPS:
                conn = http.HTTPSConnection(TacytAuth.API_HOST, TacytAuth.API_PORT)
            else:
                conn = http.HTTPConnection(TacytAuth.API_HOST, TacytAuth.API_PORT)

        try:
            all_headers = auth_headers
            if method == "POST" or method == "PUT":
                all_headers["Content-type"] = "application/json"

            if body is not None:
                conn.request(method=method, url=url, body=json_body, headers=all_headers)
            else:
                conn.request(method, url, headers=auth_headers)

            response = conn.getresponse()

            response_data = response.read().decode('utf8')

            conn.close()
            ret = TacytResponse(response_data)
        except Exception, e:
            print "Exception"
            print e
            print repr(e)
            ret = None

        return ret

    def sign_data(self, data):
        '''
        @param $data the string to sign
        @return string base64 encoding of the HMAC-SHA1 hash of the data parameter using {@code secretKey} as cipher key.
        '''
        from hashlib import sha1
        import hmac
        import binascii

        sha1_hash = hmac.new(self.secretKey.encode(), data.encode(), sha1)
        return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')

    def authentication_headers(self, http_method, query_string, x_headers=None, utc=None, params=None):
        '''
        Calculate the authentication headers to be sent with a request to the API
        @param $http_method the HTTP Method, currently only GET is supported
        @param $query_string the urlencoded string including the path (from the first forward slash) and the parameters
        @param $x_headers HTTP headers specific to the 11-paths API. null if not needed.
        @param $utc the Universal Coordinated Time for the Date HTTP header
        @return array a map with the Authorization and Date headers needed to sign a Tacyt API request
        '''

        if not utc:
            utc = TacytAuth.get_current_UTC()

        utc = utc.strip()

        #logging.debug(http_method)
        #logging.debug(query_string)
        #logging.debug(utc)



        string_to_sign = (http_method.upper().strip() + "\n" +
                          utc + "\n" +
                          self.get_serialized_headers(x_headers) + "\n" +
                          query_string.strip())


        #if params is not None:
            #string_to_sign = string_to_sign + "\n" + self.get_serialized_params(params)
            #string_to_sign = string_to_sign + "\n" + str(params).strip()

        authorization_header = (TacytAuth.AUTHORIZATION_METHOD + TacytAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.appId + TacytAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.sign_data(string_to_sign))


        headers = dict()
        headers[TacytAuth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[TacytAuth.DATE_HEADER_NAME] = utc

        return headers


    def authentication_headers_with_body(self, http_method, query_string, x_headers=None, body=None, utc=None):
        """

        """
        body_hash = None
        if body is not None:
            body_hash = hashlib.sha1(str(body)).hexdigest()
            if x_headers is None:
                x_headers = dict()
            x_headers[TacytAuth.BODY_HASH_HEADER_NAME] = body_hash

        if not utc:
            utc = TacytAuth.get_current_UTC()

        utc = utc.strip()

        string_to_sign = (http_method.upper().strip() + "\n" +
                          utc + "\n" +
                          self.get_serialized_headers(x_headers) + "\n" +
                          query_string.strip())

        #not params

        authorization_header = (TacytAuth.AUTHORIZATION_METHOD + TacytAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.appId + TacytAuth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
                                self.sign_data(string_to_sign))

        headers = dict()
        headers[TacytAuth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[TacytAuth.DATE_HEADER_NAME] = utc
        if body_hash is not None:
            headers[TacytAuth.BODY_HASH_HEADER_NAME] = body_hash

        return headers





    def get_serialized_headers(self, x_headers):
        '''
        Prepares and returns a string ready to be signed from the 11-paths specific HTTP headers received
        @param $x_headers a non neccesarily ordered map (array without duplicates) of the HTTP headers to be ordered.
        @return string The serialized headers, an empty string if no headers are passed, or None if there's a problem such as non 11paths specific headers
        '''
        if x_headers:
            headers = dict((k.lower(), v) for k, v in x_headers.iteritems())
            #headers.sort()
            serialized_headers = ""
            for key, value in headers.iteritems():
                if not key.startswith(TacytAuth.X_11PATHS_HEADER_PREFIX.lower()):
                    logging.error(
                        "Error serializing headers. Only specific " + TacytAuth.X_11PATHS_HEADER_PREFIX + " headers need to be singed")
                    return None
                serialized_headers += key + TacytAuth.X_11PATHS_HEADER_SEPARATOR + value + " "
            return serialized_headers.strip()
        else:
            return ""

    def get_serialized_params(self, params):
        """

        @params
        """
        try:
            # Try to use the new Python3 HTTP library if available
            import http.client as http
            import urllib.parse as urllib
        except:
            # Must be using Python2 so use the appropriate library
            import httplib as http
            import urllib
        if params:
            serialized_params = ""
            for key in sorted(params):
                serialized_params += key + "=" + urllib.quote_plus(params[key]) + "&"
            return serialized_params.strip("&")
        else:
            return ""