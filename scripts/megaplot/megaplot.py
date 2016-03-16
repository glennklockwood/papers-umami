#!/usr/bin/env python

import sys
import os
import string

from darshan_analyzer import darshan_analyze
from lmt_analyzer import lmt_analyze

darshan_logfile = sys.argv[1]

# analyze darshan log data and generate output file
# NOTE: darshan returns a job start time and job id that are
#       neededed to analyze data from other sources (LMT, etc)
darshan_dat_strm = open("darshan_plot.dat", "w")
job_start_tm, job_id = darshan_analyze(darshan_logfile, darshan_dat_strm)

print job_start_tm
print job_id
