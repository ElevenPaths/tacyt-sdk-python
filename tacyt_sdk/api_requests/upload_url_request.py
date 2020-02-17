"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2019 Eleven Paths
"""


class UploadUrlRequest:
    def __init__(self, urls, tag_names=None):
        self.urls = urls
        self.tag_names = tag_names

    def as_dict(self):
        json_data = dict()
        if self.urls is not None:
            json_data["urls"] = self.urls
        if self.tag_names is not None:
            json_data["tagNames"] = self.tag_names
        return json_data
