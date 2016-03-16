#!/usr/bin/env python

import datetime
import csv


'''
Class for storing gnuplot data for LMT logs
'''
class LMTOSTData:
    def __init__(self):
        self.test = 0

'''
lmt_analyze()

'''
def lmt_analyze(job_start_tm, job_duration, out_stream):
