#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class Analyzer(object):
    '''
    Class for analyzing a data source and generating gnuplot data file
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def analyze_data(self, param):
        pass
