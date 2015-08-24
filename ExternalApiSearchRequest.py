#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''

from ExternalApiRequest import ExternalApiRequest
import StringIO
import Error
import json


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
            string_builder = StringIO.StringIO()
            for field in outputFields:
                string_builder.write(field + ",")

            outputFields = str(string_builder)

        self.grouped = grouped
        self.query = query

    def get_json_encode_for_search(self):

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
