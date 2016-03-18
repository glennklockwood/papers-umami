#!/usr/bin/env python

import subprocess
import csv

'''
Class for storing gnuplot data for a Darshan log
'''
class DarshanRankData:
    def __init__(self):
        self.read_start = 0
        self.write_start = 0
        self.read_end = 0
        self.write_end = 0
    def update(self, read_start, write_start, read_end, write_end):
        if (read_start > 0 and self.read_start == 0) or (
                read_start < self.read_start):
            self.read_start = read_start
        if (write_start > 0 and self.write_start == 0) or (
                write_start < self.write_start):
            self.write_start = write_start
        if read_end > self.read_end:
            self.read_end = read_end
        if write_end > self.write_end:
            self.write_end = write_end

'''
darshan_analyze()

Function that takes an input Darshan logfile path and
generates a corresponding gnuplot data file to use for
plotting Darshan I/O intervals
'''
def darshan_analyze(logfile_name, out_stream):
    parser_output = subprocess.check_output(['darshan-parser', logfile_name])

    rank_data = {}
    job_id, job_start_tm, job_run_tm = _darshan_build_rank_data(parser_output, rank_data)

    out_field_names = ['RANK', 'READ_START', 'WRITE_START', 'READ_END', 'WRITE_END']
    writer = csv.DictWriter(out_stream, out_field_names, delimiter=',')
    writer.writeheader()

    for rank in sorted(rank_data):
        # append this rank's data to the output csv stream
        writer.writerow({
            'RANK': rank,
            'READ_START': rank_data[rank].read_start,
            'WRITE_START': rank_data[rank].write_start,
            'READ_END': rank_data[rank].read_end,
            'WRITE_END': rank_data[rank].write_end})

    return (job_id, job_start_tm, job_run_tm)


'''
helper function for building dictionary of DarshanRankData
structures for each active rank in the application
'''
def _darshan_build_rank_data(parser_output, rank_data):
    prev_rec_id = 0
    read_start = 0
    write_start = 0
    read_end = 0
    write_end = 0

    for line in parser_output.split('\n'):
        if not line.strip():
            continue # skip empty line
        elif line.startswith('#'):
            if "start_time:" in line:
                job_start_tm = int(line.split(' ')[2])
            elif "jobid" in line:
                job_id = line.split(' ')[2]
            elif "run time" in line:
                job_run_tm = int(line.split(' ')[3])
        else:
            fields = line.split('\t')
            module = fields[0]
            rec_id = fields[1] + fields[2]

            if module != "POSIX":
                break

            if rec_id != prev_rec_id and prev_rec_id != 0:
                if read_start > 0 or write_start > 0 or read_end > 0 or write_end > 0:
                    # add/update dictionary entry
                    if rank not in rank_data:
                        rank_data[rank] = DarshanRankData()
                    rank_data[rank].update(read_start, write_start, read_end, write_end);
                    read_start = 0
                    write_start = 0
                    read_end = 0
                    write_end = 0
            prev_rec_id = rec_id

            rank = int(fields[1])
            counter = fields[3]
            value = float(fields[4])

            # grab relevant counter data, rounding to nearest integer
            # since we have no need for greater precision than seconds
            if counter == "POSIX_F_READ_START_TIMESTAMP" and value > 0.0:
                read_start = int(round(value)) + job_start_tm
            elif counter == "POSIX_F_WRITE_START_TIMESTAMP" and value > 0.0:
                write_start = int(round(value)) + job_start_tm
            elif counter == "POSIX_F_READ_END_TIMESTAMP" and value > 0.0:
                read_end = int(round(value)) + job_start_tm
            elif counter == "POSIX_F_WRITE_END_TIMESTAMP" and value > 0.0:
                write_end = int(round(value)) + job_start_tm

    if prev_rec_id != 0:
        if read_start > 0 or write_start > 0 or read_end > 0 or write_end > 0:
            # add/update dictionary entry for the very last record
            if rank not in rank_data:
                rank_data[rank] = DarshanRankData()
            rank_data[rank].update(read_start, write_start, read_end, write_end);

    return (job_id, job_start_tm, job_run_tm)
