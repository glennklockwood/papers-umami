#!/usr/bin/env python

import sys
import os
import string

from darshan_analyzer import darshan_analyze
from lmt_analyzer import lmt_analyze
from slurm_analyzer import slurm_analyze

darshan_logfile = sys.argv[1]

# analyze darshan log data and generate output plot file
# NOTE: darshan returns a job start time and job id that are
#       neededed to analyze data from other sources (LMT, etc)
darshan_dat_strm = open("darshan_plot.dat", "w")
job_id, job_start_tm, job_run_tm = darshan_analyze(darshan_logfile, darshan_dat_strm)

# analyze lmt logs and generate output plot file
#lmt_analyze(job_start_tm, job_start_tm + job_run_tm, sys.stdout)

slurm_dat_strm = open("slurm_plot.dat", "w")
slurm_analyze(job_id, job_start_tm, job_start_tm + job_run_tm, slurm_dat_strm)
