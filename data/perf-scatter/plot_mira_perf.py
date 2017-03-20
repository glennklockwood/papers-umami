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

### Generate scatter plots to visualize the relationships between performance
### and ggiostat measurements
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
    title_str = "Coefficient=%.4f, P-value=%.2g" \
                    % stats.pearsonr(x, y)
#                   % stats.spearmanr(x, y)
    ax.set_title(title_str, fontsize=12 )
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.grid(True)

    if counter_name.startswith('ggio_'):
        output_file = 'perf_vs_%s.png' % counter_name.split('_', 1)[1]
    else:
        output_file = 'perf_vs_%s.png' % counter_name
    print "Generating %s (%s)" % (output_file, title_str)
    fig.savefig(output_file, bbox_inches='tight')

### Calculate the Pearson correlation coefficient and the associated
### p-value for every permutation of counter pairs
pearson_results = []
for i in range(len(df.columns) - 1):
    i_name = df.columns[i]
    for j in range(i, len(df.columns)):
        j_name = df.columns[j]
        try:
            coeff, pval = stats.pearsonr(df[i_name], df[j_name])
            pearson_results.append((i_name, j_name, coeff, pval))
        except TypeError:
            ### when passing non-numeric arguments to stats.pearsonr
            pass

### Now print the calculated Pearson correlations by the lowest p-values
only_print_key = 'agg_perf_by_slowest' # only care about performance correlation
print "%10s %10s %30s : %-15s" % ("P.Coeff", "P-val", "Counter1", "Counter2")
for (col_name1, col_name2, coeff, pval) in sorted(pearson_results, key=lambda x: x[3]):
    ### don't print trivial relationships
    if pval == 0 or pval == 1:
        continue
    ### don't print relationships with very high p-values
    if pval > 0.05:
        continue
    ### don't correlate data from the same source since much of it is degenerate
    if col_name1.split('_',1)[0] == col_name2.split('_',1)[0]:
        continue
    ### don't print anything except for the key of interest (if provided)
    if only_print_key is not None \
    and col_name1 != only_print_key \
    and col_name2 != only_print_key:
        continue
    print "%10.4f %10.4g %30s : %-15s" % (coeff, pval, col_name1, col_name2)
