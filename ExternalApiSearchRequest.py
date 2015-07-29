#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''

from tacyt.ExternalApiRequest import ExternalApiRequest
from cStringIO import StringIO
from Error import Error
import json

class StringBuilder():
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def append(self, str):
        self._file_str.write(str)

    def __str__(self):
        return self._file_str.getvalue()


class ExternalApiSearchRequest(ExternalApiRequest):

    grouped = None
    numberPage = 1
    maxResults = 20
    query = None
    outputFields = None

    def __init__(self, query=None, numberPage=None, maxResults=None, outputFields=None, grouped=None):

        if (numberPage <= 0):
            numberPage = 1

        if (maxResults <= 0):
            maxResults = 20

        if (outputFields != None and len(outputFields) > 0):
            string_builder = StringBuilder()
            for field in outputFields:
                string_builder.append(field)

            outputFields = str(string_builder)

        grouped = False
        self.query = query

    def get_json_encode(self):

        json_data = dict()
        if self.query is not None:
            json_data["query"] = self.query
        if self.numberPage is not None:
            json_data["numberPage"] = self.numberPage
        if self.maxResults is not None:
            json_data["maxResults"] = self.maxResults
        if self.outputFields is not None:
            json_data["outputFields"] = self.outputFields
        if self.grouped is not None:
            json_data["grouped"] = self.grouped

        return json_data

    def get_from_json(self, json):
        json_object = json.loads(json)
        if "data" in json_object:
            self.data = json_object["data"]
            return self.data
        else:
            self.data = ""
            return self.data

        if "error" in json_object:
            self.error = Error(json_object["error"])
            return self.error
        else:
            self.error = ""
            return self.error



















