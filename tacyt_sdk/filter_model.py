"""
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015-2020 Eleven Paths
"""


class Filter(object):
    class Rule(object):
        def __init__(self, weight=None, content=None):
            self.weight = weight
            self.content = content

        def as_dict(self):
            return {"weight": self.weight, "content": self.content}

    PUBLIC_VISIBILITY = "PUBLIC"
    PRIVATE_VISIBILITY = "PRIVATE"

    def __init__(self, filter_id=None, name=None, description=None, weight=None,
                 visibility=None, rules=None, groups=None):
        self.filter_id = filter_id
        self.name = name
        self.description = description
        self.weight = weight
        self.visibility = visibility
        self.rules = rules if rules else []
        self.groups = groups

    def as_dict(self):
        result = {"id": self.filter_id,
                  "name": self.name,
                  "description": self.description,
                  "weight": self.weight,
                  "visibility": self.visibility,
                  "rules": self.rules,
                  "groups": self.groups}

        filter_rules = [rule.as_dict() for rule in self.rules]
        if filter_rules:
            result["rules"] = filter_rules
        return result
