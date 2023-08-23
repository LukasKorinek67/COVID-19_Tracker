#!/bin/env python
# -*- coding: utf-8 -*-

"""
STI - Controller
"""

import datetime

class DailyCasesData():

    def __init__(self, date, published_mz = None, daily_gain_mz = None, total_amount_mz = None, published_who = None, daily_gain_who = None, total_amount_who = None, diff_daily_gain = None, diff_total_amount = None, diff_time = None):
        self.date = date
        self.published_mz = published_mz
        self.daily_gain_mz = daily_gain_mz
        self.total_amount_mz = total_amount_mz
        self.published_who = published_who
        self.daily_gain_who = daily_gain_who
        self.total_amount_who = total_amount_who
        if diff_daily_gain == None:
            self.diff_daily_gain = self.calculate_diff_daily_gain()
        else:
            self.diff_daily_gain = diff_daily_gain
        
        if diff_total_amount == None:
            self.diff_total_amount = self.calculate_diff_total()
        else:
            self.diff_total_amount = diff_total_amount
        
        if diff_time == None:
            self.diff_time = self.calculate_diff_time()
        else:
            self.diff_time = diff_time

    def calculate_diff_daily_gain(self):
        if self.daily_gain_mz is None or self.daily_gain_who is None:
            return None
        else:
            return abs(self.daily_gain_who - self.daily_gain_mz)

    def calculate_diff_total(self):
        if self.total_amount_mz is None or self.total_amount_who is None:
            return None
        else:
            return abs(self.total_amount_who - self.total_amount_mz)

    def calculate_diff_time(self):
        if self.published_mz is None or self.published_who is None:
            return None
        else:
            diff = self.published_who - self.published_mz
            diff = diff - datetime.timedelta(microseconds=diff.microseconds)
            return diff
