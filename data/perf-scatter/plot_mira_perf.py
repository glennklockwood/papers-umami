#!/usr/bin/env python

import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import pandas

matplotlib.rcParams.update({'font.size': 12})

### Load the CSV data file
TOKIO_HOME = os.path.realpath(os.path.join( os.path.dirname(__file__), '..', '..'))

if len(sys.argv) < 2:
    csv_file = os.path.join(TOKIO_HOME, 'data', 'dat', 'tokio-gpfs', 'alcf-abc-stats_2-25_3-19.dat')
else:
    csv_file = sys.argv[1]

print "Loading %s" % csv_file
df = pandas.DataFrame.from_csv(csv_file).dropna()


### Calculate the coverage factor
df['coverage_factor'] = df['total_bytes'].values / (df['ggio_bytes_read'] + df['ggio_bytes_written'])

### Drop rows where the coverage factor is > 2; these rows have data missing
df = df[df['coverage_factor'] < 2.0]

for counter_name in [ x for x in df.keys() if x.startswith('ggio_') ] \
               + ['coverage_factor']:
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    
    x = df['agg_perf_by_slowest'].values
    x_label = 'agg_perf_by_slowest'
    y = df[counter_name].values
    y_label = counter_name 
    ax.plot(x, y, 'o', alpha=0.5)

    ### attempt a linear fit to generate a visual aid
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x+b, "-")
    
    ### add window dressing to plots
#   fig.suptitle('Correlation between %s and %s' 
#                 % (x_label.split('(',1)[0].strip(),
#                    y_label.split('(',1)[0].strip()))
    ax.set_title("Coefficient=%.4f, P-value=%.2g" 
                    % stats.pearsonr(x, y), fontsize=12 )
#                   % stats.spearmanr(x, y), fontsize=12 )
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.grid(True)

    if counter_name.startswith('ggio_'):
        output_file = 'perf_vs_%s.pdf' % counter_name.split('_', 1)[1]
    else:
        output_file = 'perf_vs_%s.pdf' % counter_name
    print "Generating %s" % output_file
    fig.savefig(output_file, bbox_inches='tight')
