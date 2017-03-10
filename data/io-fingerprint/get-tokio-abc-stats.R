source("utils.R")
source("stats.R")
source("aes.R")

#normalize <- function(x) {
#     a <- min(x) 
#     b <- max(x) 
#     (x - a)/(b - a)
#}

normalize <- function(x) {
     m <- max(x) 
     x / m
}

alcf_perf <- read.csv("../dat/alcf_2-9_3-1.dat", header=TRUE, sep=',', col.names=c("sys", "fs", "app", "api", "op", "time", "rate", "size", "start", "end", "jobid"))

# split results into read/write tables
alcf_perf_tables <- split(alcf_perf, alcf_perf$op)

# normalize rates
alcf_perf_tables$write["rate"] <- as.data.frame(lapply(alcf_perf_tables$write["rate"], normalize))
alcf_perf_tables$read["rate"] <- as.data.frame(lapply(alcf_perf_tables$read["rate"], normalize))

alcf_write_perf_stats <- CalculateDataSummary(data=alcf_perf_tables$write, measurevar="rate", groupvars=c("sys", "fs", "app", "api", "op"), conf.interval=.95, quantile.interval=.95)
alcf_read_perf_stats <- CalculateDataSummary(data=alcf_perf_tables$read, measurevar="rate", groupvars=c("sys", "fs", "app", "api", "op"), conf.interval=.95, quantile.interval=.95)

print(alcf_write_perf_stats)
print(alcf_read_perf_stats)

nersc_perf <- read.csv("../dat/nersc_2-14_3-1.dat", header=TRUE, sep=',', col.names=c("sys", "fs", "app", "api", "op", "time", "rate", "size", "start", "end", "jobid"))

# split results into read/write tables
nersc_perf_tables <- split(nersc_perf, list(nersc_perf$fs, nersc_perf$op))

# normalize rates
nersc_perf_tables$scratch1.write["rate"] <- as.data.frame(lapply(nersc_perf_tables$scratch1.write["rate"], normalize))
nersc_perf_tables$scratch1.read["rate"] <- as.data.frame(lapply(nersc_perf_tables$scratch1.read["rate"], normalize))

nersc_write_perf_stats <- CalculateDataSummary(data=nersc_perf_tables$scratch1.write, measurevar="rate", groupvars=c("sys", "fs", "app", "api", "op"), conf.interval=.95, quantile.interval=.95)
nersc_read_perf_stats <- CalculateDataSummary(data=nersc_perf_tables$scratch1.read, measurevar="rate", groupvars=c("sys", "fs", "app", "api", "op"), conf.interval=.95, quantile.interval=.95)

print(nersc_write_perf_stats)
print(nersc_read_perf_stats)

# write data out to separate read and write files
write.table(alcf_write_perf_stats, file="io-fingerprint-dat/write-perf-stats.dat", row.names=FALSE)
write.table(nersc_write_perf_stats, file="io-fingerprint-dat/write-perf-stats.dat", row.names=FALSE, col.names=FALSE, append=TRUE)

write.table(alcf_read_perf_stats, file="io-fingerprint-dat/read-perf-stats.dat", row.names=FALSE)
write.table(nersc_read_perf_stats, file="io-fingerprint-dat/read-perf-stats.dat", row.names=FALSE, col.names=FALSE, append=TRUE)
