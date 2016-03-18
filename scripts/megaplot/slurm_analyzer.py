#!/usr/bin/env python

import subprocess
import time
import csv

'''
Class for storing gnuplot data for a Slurm job
'''
class SlurmJobData:
    def __init__(self, job_start_tm, job_end_tm, job_nnodes):
        self.job_start_tm = job_start_tm
        self.job_end_tm = job_end_tm
        self.job_nnodes = job_nnodes

def slurm_analyze(job_id, job_start_tm, job_end_tm, out_stream):
    slurm_start_tm = time.strftime("%m/%d/%y-%H:%M:%S",
        time.localtime(job_start_tm - (48 * 60 * 60))) # job start minus 48 hour max run time
    slurm_end_tm = time.strftime("%m/%d/%y-%H:%M:%S",
        time.localtime(job_end_tm + (48 * 60 * 60))) # job end plus 48 hour max run time

    sacct_output = subprocess.check_output(['sacct',
        '--allusers',
        '--starttime=' + slurm_start_tm,
        '--endtime=' + slurm_end_tm,
        '--state=CD',
        '--noheader',
        '--format=JobID,AllocNodes,AllocCPUs,Start,End'])

    job_data = {}
    _slurm_build_job_data(sacct_output, job_id, job_start_tm, job_end_tm, job_data)

    out_field_names = ['JOB_ID', 'JOB_START', 'JOB_END', 'JOB_NNODES']
    writer = csv.DictWriter(out_stream, out_field_names, delimiter=',')
    writer.writeheader()

    for job_id in job_data:
        # append this job's data to the output csv stream
        writer.writerow({
            'JOB_ID': job_id,
            'JOB_START': job_data[job_id].job_start_tm,
            'JOB_END': job_data[job_id].job_end_tm,
            'JOB_NNODES': job_data[job_id].job_nnodes})


def _slurm_build_job_data(sacct_output, target_job_id, target_job_start_tm,
target_job_end_tm, job_data):
    sacct_time_fmt = "%Y-%m-%dT%H:%M:%S"

    for line in sacct_output.split('\n'):
        if not line.strip():
            continue # skip empty line

        fields = line.split()
        job_id = fields[0]
        if '.' in job_id:
            continue # skip individual job steps, just grab complete job data
        if job_id == target_job_id:
            continue # skip ourselves
        job_nnodes = int(fields[1])
        job_ncores = int(fields[2])
        job_start_tm = int(time.mktime(time.strptime(fields[3], sacct_time_fmt)))
        job_end_tm = int(time.mktime(time.strptime(fields[4], sacct_time_fmt)))

        if target_job_start_tm <= job_end_tm and target_job_end_tm >= job_start_tm:
            assert (job_id not in job_data), "Duplicate Slurm job ids"
            job_data[job_id] = SlurmJobData(job_start_tm, job_end_tm, job_nnodes)
