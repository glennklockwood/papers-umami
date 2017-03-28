#!/usr/bin/env python

import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_gpfs_coverage(job):
    t_g_start = job['start_time'] + 5 - (job['start_time'] % 5)
    t_g_end = job['end_time'] + 5 - (job['end_time'] % 5)
    n_ints = ((t_g_end - t_g_start) / 5) + 1
    ratios = np.ones(n_ints)
    ratios[0] = (t_g_start - job['start_time']) / float(5.0)
    ratios[-1] -= (t_g_end - job['end_time']) / float(5.0)

    job_gpfs_df = gpfs_df.loc[(gpfs_df.index >= t_g_start) & (gpfs_df.index <= t_g_end)]
    if len(job_gpfs_df.index) < n_ints:
        return pd.DataFrame(np.nan, index=[1], columns=gpfs_df.columns).iloc[0]

    job_ali_gpfs_df = np.rint(job_gpfs_df.mul(ratios, axis=0))
    return job_ali_gpfs_df.sum()

if __name__ == "__main__":
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    gpfs_df = pd.read_csv('mira-fs1_2-25_3-28_merged.dat')
    gpfs_df = gpfs_df.set_index('SECONDS')

    abc_df = pd.read_csv('../tokio-abc/alcf_2-9_3-27.dat', header=0)

    abc_df = abc_df.join(abc_df.apply(calc_gpfs_coverage, axis=1))
    abc_df = abc_df.rename(columns={'BYTES_READ': 'ggio_bytes_read', \
        'BYTES_WRITTEN': 'ggio_bytes_written', 'OPEN_COUNT': 'ggio_opens', \
        'CLOSE_COUNT': 'ggio_closes', 'READ_REQUESTS': 'ggio_read_reqs', \
        'WRITE_REQUESTS': 'ggio_write_reqs', 'READ_DIRECTORY': 'ggio_read_dirs', \
        'INODE_UPDATES': 'ggio_inoded_updates'})
    abc_df.to_csv('alcf-abc-stats_2-25_3-27.dat')
