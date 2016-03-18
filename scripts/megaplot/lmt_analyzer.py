#!/usr/bin/env python

import h5py
import pandas
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
def lmt_analyze(job_start_tm, job_end_tm, out_stream):
    _DELTA_TIME = 5 # LMT monitoring interval
    _TARGET_DATASETS = [
        ('OSTReadGroup/OSTBulkReadDataSet',   'ost-read.csv'),
        ('OSTWriteGroup/OSTBulkWriteDataSet', 'ost-write.csv'),
    ]

    h5lmtfile = "/global/project/projectdirs/pma/www/daily/2016-03-14/cori_snx11168.h5lmt"

    # open the h5lmt file we want to extract data from
    # XXX: this does not account for jobs that run across midnight!
    f = h5py.File(h5lmtfile, 'r')

    # determine valid buckets to get LMT data from using the
    # application start time and duration
    idx_0 = (int(job_start_tm) % 86400) / _DELTA_TIME
    idx_f = (int(job_start_tm + job_end_tm) % 86400) / _DELTA_TIME + 1
    t_startofday = int(int(job_start_tm) / 86400) * 86400

    # XXX: plus 1?
    timestamps = [(t_startofday + _DELTA_TIME * t) for t in range(idx_0, idx_f + 1)]

    for dataset, outfile in _TARGET_DATASETS:
        df = pandas.DataFrame(None, index=timestamps)
        df.index.name = 'timestamp'
        row_id = 0
        for one_row in f[dataset]:
            record = one_row[idx_0:idx_f+1]
            label = "%s%d" % (outfile.split('-',1)[0], row_id)
            df[label] = record
            row_id += 1
        df.to_csv(outfile)
