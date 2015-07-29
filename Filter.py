__author__ = 'ruben.moreno'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015 Eleven Paths
'''

class Filter():

    class Rule():

        weight = None
        content = None

        def __init__(self, weight=None, content=None):
            self.weight = weight
            self.content = content

        def get_weight(self):
            self.weight

        def get_content(self):
            self.content

    class Visibility():

        PUBLIC = "PUBLIC"
        PRIVATE = "PRIVATE"

        def get_default(self):
            return self.PRIVATE

        def to_string(self):
            return self.upper()

    id = None
    app_id = None
    user = None
    name = None
    description = None
    alias = None
    weight = None
    visibility = Visibility().get_default()
    rules = [Rule(None, None)]
    number_of_subscriptions = None

    def get_app_id(self):
        return self.app_id

    def get_user(self):
        return self.user

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_alias(self):
        self.alias

    def get_weight(self):
        self.weight

    def get_visibility(self):
        self.visibility

    def get_rules(self):
        self.rules

    def get_number_of_subscriptions(self):
        return self.number_of_subscriptions

    def __init__(self, id=None, name=None, description=None, weight=None, visibility=None, rules=None):
        self.id = id
        self.name = name
        self.description = description
        self.weight = weight
        self.visibility = visibility
        self.rules = rules



