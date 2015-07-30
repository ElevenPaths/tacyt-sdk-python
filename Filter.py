
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

    PUBLIC_VISIBILITY = "PUBLIC"
    PRIVATE_VISIBILITY = "PRIVATE"

    id = None
    name = None
    description = None
    weight = None
    visibility = PRIVATE_VISIBILITY
    rules = [Rule(None, None)]

    def __init__(self, id=None, name=None, description=None, weight=None, visibility=None, rules=None):
        self.id = id
        self.name = name
        self.description = description
        self.weight = weight
        self.visibility = visibility
        self.rules = rules
