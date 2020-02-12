#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2020 Eleven Paths
"""


def to_camel_case(field_name):
    name_parts = field_name.split("_")
    camel_case = "".join(char.capitalize() for char in name_parts[1:])
    camel_case = name_parts[0] + camel_case
    return camel_case


class ExternalApiMarketNewAppRequest:
    def __init__(self, unique_origin_id, unique_version_id, platform,
                 origin, title, app_url, **extra_arguments):
        self.unique_origin_id = unique_origin_id
        self.unique_version_id = unique_version_id
        self.platform = platform
        self.origin = origin
        self.title = title
        self.app_url = app_url
        self.extra_aguments = extra_arguments

    def get_json_encode_for_new_market_app(self):
        json_dict = {
            "uniqueOriginId": self.unique_origin_id,
            "uniqueVersionId": self.unique_version_id,
            "platform": self.platform,
            "origin": self.origin,
            "title": self.title,
            "appURL": self.app_url
        }

        for field_name in self.extra_arguments:
            camel_case_name = to_camel_case(field_name)
            json_dict[camel_case_name] = self.extra_aguments[field_name]
        return json_dict


class ExternalApiMarketUpdateAppRequest:
    def __init__(self, unique_origin_id, unique_version_id, origin,
                 **extra_arguments):
        self.unique_origin_id = unique_origin_id
        self.unique_version_id = unique_version_id
        self.origin = origin
        self.extra_arguments = extra_arguments

    def _to_camel_case(self, field_name):
        if field_name == "app_url":
            return "appURL"
        return to_camel_case(field_name)

    def get_json_encode_for_new_market_app(self):
        json_dict = {
            "uniqueOriginId": self.unique_origin_id,
            "uniqueVersionId": self.unique_version_id,
            "origin": self.origin,
        }

        for field_name in self.extra_arguments:
            camel_case_name = self._to_camel_case(field_name)
            json_dict[camel_case_name] = self.extra_aguments[field_name]
        return json_dict

