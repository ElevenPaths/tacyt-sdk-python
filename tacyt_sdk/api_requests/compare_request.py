"""
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
"""


class CompareRequest(object):
    FIELD_MATCHING_FIELDS = "matchingFields"
    FIELD_MATCHING_QUERY = "matchingQuery"
    FIELD_APPS = "apps"

    def __init__(self, apps, include_details):
        self.apps = apps if apps else []
        self.include_details = include_details

    def as_dict(self):
        data = dict()
        if self.apps is not None:
            data["apps"] = self.apps
        if self.include_details is not None:
            data["includeDetails"] = self.include_details
        return data
