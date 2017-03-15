#!/usr/bin/env python

import sys
import math
from subprocess import Popen, PIPE
import pandas
import numpy

_INTERVAL_LEN=5

def usage():
    print 'Usage: merge-gpfs-clusters.py <mmpmon_file_0 mmpmon_file_1 ...>'
    exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    agg_t_start = -1
    agg_t_end = -1
    gpfs_cluster_df = {}
    for dat_log in sys.argv[1:]:
        gpfs_cluster_df[dat_log] = pandas.read_csv(dat_log, sep='\s+', dtype=numpy.int64, skiprows={1})
        if agg_t_start == -1 or agg_t_start < gpfs_cluster_df[dat_log].iloc[0]['SECONDS']:
            agg_t_start = gpfs_cluster_df[dat_log].iloc[0]['SECONDS']
        if agg_t_end == -1 or agg_t_end > gpfs_cluster_df[dat_log].iloc[-1]['SECONDS']:
            agg_t_end = gpfs_cluster_df[dat_log].iloc[-1]['SECONDS']

    agg_t_start = int(math.ceil(agg_t_start / float(_INTERVAL_LEN)) * _INTERVAL_LEN)
    agg_t_end = int(math.floor(agg_t_end / float(_INTERVAL_LEN)) * _INTERVAL_LEN)
    n_intervals = int((agg_t_end - agg_t_start) / _INTERVAL_LEN)
    print agg_t_start, agg_t_end, n_intervals

    agg_df = pandas.DataFrame(0, index=numpy.arange(n_intervals), \
        columns=gpfs_cluster_df[sys.argv[1]].columns)
    agg_df['SECONDS'] = range(agg_t_start + _INTERVAL_LEN, agg_t_end + _INTERVAL_LEN, _INTERVAL_LEN)
    agg_df = agg_df.set_index('SECONDS')
    sum_df = pandas.DataFrame(0, index=numpy.arange(1), columns=agg_df.columns)

    for dat_log in sys.argv[1:]:
        print dat_log
        df = gpfs_cluster_df[dat_log].set_index('SECONDS')
        sum_df += df.sum()

        for ndx, row in df.iterrows():
            if ndx <= agg_t_start or t_prev >= agg_t_end:
                t_prev = ndx
                row = row * 0
            else:
                assert (t_prev < ndx), \
                    "unexpected timestamp (%d after %d) encountered in file %s" % \
                    (ndx, t_prev, dat_log)

                row_t_dur = ndx - t_prev
                ival_start = t_prev
                while ival_start < ndx and ival_start < agg_t_end:
                    ival_end = min(int((math.floor(ival_start / float(_INTERVAL_LEN)) + 1) * _INTERVAL_LEN), ndx)
                    #print ival_start, ival_end, row_t_dur
                    if ival_start < agg_t_start:
                        row = row.apply(lambda x: x - int(math.floor(x * (ival_end - ival_start) / float(row_t_dur))))
                    else:
                        ival_row = row.apply(lambda x: int(math.floor(x * (ival_end - ival_start) / float(row_t_dur))))
                        row = row - ival_row
                        agg_ndx = int((math.floor(ival_start / float(_INTERVAL_LEN)) + 1) * _INTERVAL_LEN)
                        agg_df.loc[agg_ndx] += ival_row
                    row_t_dur -= (ival_end - ival_start)
                    ival_start = ival_end
                t_prev = ival_end

            df.loc[ndx] = row
#            if df.loc[ndx]['INODE_UPDATES'] > 0:
#                print df.loc[ndx]
#        #print df

    print sum_df
    print "****"
    print agg_df.sum()
    #print "****"
    #print agg_df
    agg_df.to_csv("mira-fs1_2-25_3-9_merged.dat")
