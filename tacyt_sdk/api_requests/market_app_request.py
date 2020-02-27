"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""
from tacyt_sdk.utils import to_camel_case


class NewMarketAppRequest(object):
    def __init__(self, unique_origin_id, unique_version_id, platform,
                 origin, title, app_url, **extra_arguments):
        self.unique_origin_id = unique_origin_id
        self.unique_version_id = unique_version_id
        self.platform = platform
        self.origin = origin
        self.title = title
        self.app_url = app_url
        self.extra_arguments = extra_arguments

    def as_dict(self):
        data = {
            "uniqueOriginId": self.unique_origin_id,
            "uniqueVersionId": self.unique_version_id,
            "platform": self.platform,
            "origin": self.origin,
            "title": self.title,
            "appURL": self.app_url
        }

        for field_name in self.extra_arguments:
            camel_case_name = to_camel_case(field_name)
            data[camel_case_name] = self.extra_arguments[field_name]
        return data


class UpdateMarketAppRequest:
    def __init__(self, unique_origin_id, unique_version_id, origin,
                 **extra_arguments):
        self.unique_origin_id = unique_origin_id
        self.unique_version_id = unique_version_id
        self.origin = origin
        self.extra_arguments = extra_arguments

    @staticmethod
    def _to_camel_case(field_name):
        if field_name == "app_url":
            return "appURL"
        if field_name == "direct_download_url":
            return "directDownloadURL"
        return to_camel_case(field_name)

    def as_dict(self):
        data = {
            "uniqueOriginId": self.unique_origin_id,
            "uniqueVersionId": self.unique_version_id,
            "origin": self.origin,
        }
        for field_name in self.extra_arguments:
            camel_case_name = self._to_camel_case(field_name)
            data[camel_case_name] = self.extra_arguments[field_name]
        return data
