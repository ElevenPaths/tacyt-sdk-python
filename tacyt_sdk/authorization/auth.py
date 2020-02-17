# -*- coding: utf-8 -*-
import binascii
import hashlib
import hmac
import logging
from hashlib import sha1
from urllib.error import HTTPError

import requests

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


class Auth:
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

    def __init__(self, app_id, secret_key, proxy=None, use_https=True):
        """Create an instance of the class with the Application ID and
        secret obtained from Tacyt
        :param app_id: the app id part of your credentials
        :param secret_key: the secret part of your credentials
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.use_https = use_https
        self.api_host = Version.API_HOST
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
        sha1_hash = hmac.new(self.secret_key.encode(), data.encode(), sha1)
        return binascii.b2a_base64(sha1_hash.digest())[:-1].decode('utf8')

    def authentication_headers(self, http_method, query_string, headers=None,
                               body=None, utc=None):
        """Calculate the authentication headers to be sent with a request
        to the API
        :param http_method: the HTTP Method
        :param query_string: the urlencoded string including the path
        (from the first forward slash) and the parameters
        :param headers: HTTP headers specific to the 11-paths API. null if not
        needed.
        :param utc: the Universal Coordinated Time for the Date HTTP header
        :return: A dictionary with the authorization and Date headers needed
        to sign a Tacyt API request
        """

        utc = utc.strip() if utc else get_current_utc()

        if body:
            body_hash = hashlib.sha1(str(body)).hexdigest()
            headers[Auth.BODY_HASH_HEADER_NAME] = body_hash

        string_to_sign = "{http_method}\n{utc_date}\n{serialized_headers}" \
                         "\n{encoded_url}"
        string_to_sign.format(
            method=http_method.upper().strip(),
            utc_date=utc,
            serialized_headers=self.get_serialized_headers(headers),
            encoded_url=query_string
        )
        authorization_header = (
            Auth.AUTHORIZATION_METHOD +
            Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
            self.app_id +
            Auth.AUTHORIZATION_HEADER_FIELD_SEPARATOR +
            self.sign_data(string_to_sign)
        )

        headers[Auth.AUTHORIZATION_HEADER_NAME] = authorization_header
        headers[Auth.DATE_HEADER_NAME] = utc
        return headers

    @staticmethod
    def get_serialized_headers(x_headers):
        """Prepares and returns a string ready to be signed from the 11-paths
        specific HTTP headers received
        :param x_headers: a header dict of the HTTP headers
        :return: The serialized headers.
        :rtype: str
        """
        auth_headers = sorted(filter(
            lambda item: item[0].startswith(Auth.X_11PATHS_HEADER_PREFIX),
            x_headers.items()))
        return " ".join([key + " - " + value for key, value in auth_headers])

    def compose_url(self, url):
        """Compose the final url with the schema and the host of
        the api endpoint.
        :param url: the url path to the endpoint to reach
        :type url: str
        :return: A full composed http(s) url to call.
        """
        url = "https://" + self.api_host + url
        if not self.use_https:
            url = "https://" + self.api_host + url
        return url

    def http_get(self, url, headers=None):
        """Get method
        :param url:
        :param headers:
        :return:
        """
        response = None
        try:
            auth_headers = self.authentication_headers(self.HTTP_METHOD_GET,
                                                       url, headers)
            api_url = self.compose_url(url)
            res = requests.get(api_url, headers=auth_headers, proxies=self.proxy)
            res.raise_for_status()
            response = Response(json_string=res.content)
        except HTTPError as e:
            logger.error(e.message, exc_info=True)
        return response

    def http_post(self, url, headers=None, body=None):
        """
        :param url:
        :param headers:
        :param body:
        :return:
        """
        response = None
        try:
            auth_headers = self.authentication_headers(self.HTTP_METHOD_POST,
                                                       url, headers)
            api_url = self.compose_url(url)
            res = requests.post(api_url, headers=auth_headers, json=body,
                                proxies=self.proxy)
            res.raise_for_status()
            response = Response(json_string=res.content)
        except HTTPError as e:
            logger.error(e.message, exc_info=True)
        return response

    def http_put(self, url, headers=None, body=None):
        """
        :param url:
        :param headers:
        :param body:
        :return:
        """
        response = None
        try:
            auth_headers = self.authentication_headers(self.HTTP_METHOD_PUT,
                                                       url, headers)
            api_url = self.compose_url(url)
            res = requests.put(api_url, headers=auth_headers, json=body,
                               proxies=self.proxy)
            res.raise_for_status()
            response = Response(json_string=res.content)
        except HTTPError as e:
            logger.error(e.message, exc_info=True)
        return response

    def http_post_file(self, url, headers, file_stream, file_name, data=None):
        """
        :param url:
        :param headers:
        :param file_stream:
        :param file_name:
        :param data:
        :return:
        """
        response = None
        try:
            files = {'file': (file_name, file_stream, 'application/octet-stream')}
            api_url = self.compose_url(url)
            res = requests.post(api_url, headers=headers, files=files, data=data,
                                proxies=self.proxy)
            res.raise_for_status()
            response = Response(json_string=res.content)
        except HTTPError as e:
            logger.error(e.message, exc_info=True)
        return response