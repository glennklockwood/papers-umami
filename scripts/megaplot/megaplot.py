#!/usr/bin/env python

import sys

from darshan_analyzer import darshan_analyze_log

darshan_logfile = sys.argv[1]

darshan_analyze_log(darshan_logfile, sys.stdout)
