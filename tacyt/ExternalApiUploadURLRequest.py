#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2019 Eleven Paths
"""

class ExternalApiUploadURLRequest:

    def __init__(self, urls, tagNames=None):
        self.urls = urls
        self.tagNames = tagNames

    def get_json_encode_for_upload_url(self):
        json_data = dict()
        if self.urls is not None:
            json_data["urls"] = self.urls
        if self.tagNames is not None:
            json_data["tagNames"] = self.tagNames

        return json_data
