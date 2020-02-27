# -*- coding: utf-8 -*-
import binascii
import hashlib
import hmac
import json
import logging
from hashlib import sha1

import requests
from six import ensure_binary

from tacyt_sdk.authorization.error import Error
from tacyt_sdk.authorization.response import Response
from tacyt_sdk.utils import get_current_utc
from tacyt_sdk.version import Version

try:
    import http.client as http
    import urllib.parse as urllib
except ImportError:
    # Python2 compatibility
    import httplib as http
    import urllib


logger = logging.getLogger(__name__)


class Auth(object):
    AUTHORIZATION_METHOD = "11PATHS"
    X_11PATHS_HEADER_PREFIX = "X-11paths-"
    BODY_HASH_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "Body-Hash"
    AUTHORIZATION_HEADER_FIELD_SEPARATOR = " "
    CHARSET_ASCII = "US-ASCII"
    CHARSET_ISO_8859_1 = "ISO-8859-1"
    CHARSET_UTF_8 = "UTF-8"
    HTTP_METHOD_GET = "GET"
    HTTP_METHOD_POST = "POST"
    HTTP_METHOD_PUT = "PUT"
    HTTP_METHOD_DELETE = "DELETE"
    HTTP_HEADER_CONTENT_TYPE_JSON = "application/json"
    PARAM_SEPARATOR = "&"
    PARAM_VALUE_SEPARATOR = "="
    X_11PATHS_HEADER_SEPARATOR = ":"
    FILE_HASH_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "File-Hash"
    AUTHORIZATION_HEADER_NAME = "Authorization"
    DATE_HEADER_NAME = X_11PATHS_HEADER_PREFIX + "Date"

    def __init__(self, app_id, secret_key, proxy=None):
        """Create an instance of the class with the Application ID and
        secret obtained from Tacyt
        :param app_id: the app id part of your credentials
        :param secret_key: the secret part of your credentials
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.proxy = None
        if proxy:
            self.proxy = {"http": proxy, "https": proxy}

    def sign_data(self, data):
        """
        :param $data the string to sign
        :returns: base64 encoding of the HMAC-SHA1 hash of the data
        parameter using {@code secretKey} as cipher key.
        :rtype: str
        """
        sha1_hash = hmac.new(ensure_binary(self.secret_key), ensure_binary(data), sha1)
        return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')

    def authentication_headers(self, http_method, query_string, headers=None,
                               body=None, utc=None):
        """Calculate the authentication headers to be sent with a request
        to the API
        :param http_method: the HTTP Method
        :param query_string: the urlencoded string including the path
        (from the first forward slash) and the parameters
        :param headers: HTTP headers specific to the 11-paths API, excluding
        X-11Paths-Date.
        needed.
        :param body: the data that will be in the http request.
        :param utc: the Universal Coordinated Time for the Date HTTP header
        :return: A dictionary with the authorization and Date headers needed
        to sign a Tacyt API request
        """

        utc = utc.strip() if utc else get_current_utc()
        headers = headers or {}

        if body:
            body_hash = hashlib.sha1(str(body)).hexdigest()
            headers[Auth.BODY_HASH_HEADER_NAME] = body_hash

        string_to_sign = "{http_method}\n{utc_date}\n{serialized_headers}" \
                         "\n{encoded_url}"
        string_to_sign = string_to_sign.format(
            http_method=http_method.upper().strip(),
            utc_date=utc,
            serialized_headers=self.get_serialized_headers(headers),
            encoded_url=query_string.strip()
        )
        authorization_header = (
            Auth.AUTHORIZATION_METHOD +
            Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
            self.app_id +
            Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
            self.sign_data(string_to_sign)
        )

        headers[Auth.DATE_HEADER_NAME] = utc
        headers[Auth.AUTHORIZATION_HEADER_NAME] = authorization_header
        return headers

    @staticmethod
    def get_serialized_headers(x_headers):
        """Prepares and returns a string ready to be signed from the 11-paths
        specific HTTP headers received
        :param x_headers: a header dict of the HTTP headers
        :return: The serialized headers.
        :rtype: str
        """
        x_headers = x_headers or {}
        x_headers = {key.lower(): value for key, value in x_headers.items()}
        auth_headers = sorted(filter(
            lambda item: item[0].startswith(Auth.X_11PATHS_HEADER_PREFIX.lower()),
            x_headers.items()))
        return " ".join([(key.lower() + Auth.X_11PATHS_HEADER_SEPARATOR + value)
                         for key, value in auth_headers])

    def compose_url(self, url):
        """Compose the final url with the schema and the host of
        the api endpoint.
        :param url: the url path to the endpoint to reach
        :type url: str
        :return: A full composed http(s) url to call.
        """
        return "https://" + Version.API_HOST + url

    def http_get(self, url, headers=None):
        """Perform a get request to the api endpoint
        :param url: the api endpoint to perform the request including the
        query params needed.
        :param headers: extra headers if needed to pass throw the requests.
        :return: a Response object with the result
        """
        response = None
        try:
            auth_headers = self.authentication_headers(self.HTTP_METHOD_GET,
                                                       url, headers)
            api_url = self.compose_url(url)
            res = requests.get(api_url, headers=auth_headers,
                               proxies=self.proxy)
            response = Response(json_string=res.content)
            res.raise_for_status()
        except requests.HTTPError as e:
            logger.error(e.message, exc_info=True)
            if not response.error:
                response.error = Error({"code": res.status_code,
                                        "message": res.content})
        return response

    def http_post(self, url, headers=None, body=None):
        """Perform a POST request to the api endpoint
        :param url: the api endpoint to perform the request
        :param headers: extra headers if needed to pass throw the requests
        :param body: the data that should be included in the POST call
        :return: a Response object with the result
        """
        response = None
        try:
            json_body = json.dumps(body)
            auth_headers = self.authentication_headers(
                self.HTTP_METHOD_POST,
                url,
                headers,
                body=json_body)
            api_url = self.compose_url(url)
            auth_headers["Content-Type"] = "application/json"
            res = requests.post(api_url, headers=auth_headers, json=body,
                                proxies=self.proxy)
            response = Response(json_string=res.content)
            res.raise_for_status()
        except requests.HTTPError as e:
            logger.error(e.message, exc_info=True)
            if not response.error:
                response.error = Error({"code": res.status_code,
                                        "message": res.content})
        return response

    def http_put(self, url, headers=None, body=None):
        """Perform a PUT request to the api endpoint
        :param url: the api endpoint to perform the request
        :param headers: extra headers if needed to pass throw the requests
        :param body: the data that should be included in the PUT call
        :return: a Response object with the result
        """
        response = None
        try:
            auth_headers = self.authentication_headers(self.HTTP_METHOD_PUT,
                                                       url, headers)
            api_url = self.compose_url(url)
            res = requests.put(api_url, headers=auth_headers, json=body,
                               proxies=self.proxy)
            response = Response(json_string=res.content)
            res.raise_for_status()
        except requests.HTTPError as e:
            logger.error(e.message, exc_info=True)
            if not response.error:
                response.error = Error({"code": res.status_code,
                                        "message": res.content})
        return response

    def http_post_file(self, url, headers, file_stream, file_name, data=None):
        """Method to help to upload a file to the api
        :param url: the endpoint that will perform the upload
        :param headers: extra headers to include to the requests if needed
        :param file_stream: the data of the file
        :param file_name: the name of the file
        :param data: extra data if its required
        :return: a Response object with the result
        """
        response = None
        try:
            headers = self.authentication_headers(self.HTTP_METHOD_POST,
                                                  url,
                                                  headers)
            files = {'file': (file_name, file_stream,
                              'application/octet-stream')}
            api_url = self.compose_url(url)
            res = requests.post(api_url, headers=headers, files=files,
                                json=data, proxies=self.proxy)
            response = Response(json_string=res.content)
            res.raise_for_status()
        except requests.HTTPError as e:
            logger.error(e.message, exc_info=True)
        return response
