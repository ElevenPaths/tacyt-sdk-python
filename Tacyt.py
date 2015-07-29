#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TacytApp import TacytApp

class Tacyt(TacytApp):


    def __init__(self, app_id, secret_key):
        '''
        Create an instance of the class with the Application ID and secret obtained from Tacyt
        @param $app_id
        @param $secret_key
        '''
        super(Tacyt, self).__init__(app_id, secret_key)