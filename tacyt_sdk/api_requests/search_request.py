"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class SearchRequest(object):
    DEFAULT_NUMBER_PAGE = 1
    DEFAULT_MAX_RESULTS = 20

    def __init__(self, query=None, number_page=None, max_results=None,
                 output_fields=None, grouped=None):
        string_build = StringIO()
        self.number_page = (
            number_page if number_page and number_page > 1
            else SearchRequest.DEFAULT_NUMBER_PAGE)
        self.max_results = (
            max_results
            if max_results and max_results > 1
            else SearchRequest.DEFAULT_MAX_RESULTS)

        if output_fields:
            for field in output_fields:
                string_build.write(field + ",")

        self.output_fields = string_build.getvalue()
        self.grouped = grouped
        self.query = query

    def as_dict(self):
        data = dict()
        if self.query:
            data["query"] = self.query
        if self.number_page:
            data["numberPage"] = self.number_page
        if self.max_results:
            data["maxResults"] = self.max_results
        if self.output_fields:
            data["outputFields"] = self.output_fields
        if self.grouped:
            data["grouped"] = self.grouped
        return data
