set term po eps color solid 12 size 3in,1.5in
set output "mira-fs1-write-perf.eps"

set datafile separator ","

set key outside top center

set ylabel "I/O rate (GiB/s)"
set yrange [0:21]

set xdata time
set timefmt "%s"
set format x "%b-%d"
set xrange [1486533600:1488434400]
set xtics 1486533600,345600,1488434400 rotate by -45

plot "<grep IOR ../dat/alcf_2-9_3-1.dat | grep MPIIO | grep write" using 9:($7/1024) with points pt 1 title "IOR-shared-write", \
     "<grep IOR ../dat/alcf_2-9_3-1.dat | grep POSIX | grep write" using 9:($7/1024) with points pt 2 title "IOR-fpp-write", \
     "<grep HACC-IO ../dat/alcf_2-9_3-1.dat | grep write" using 9:($7/1024) with points pt 3 title "HACC-fpp-write", \
     "<grep VPIC-IO ../dat/alcf_2-9_3-1.dat" using 9:($7/1024) with points pt 4 title "VPIC-shared-write"

set output "mira-fs1-read-perf.eps"

plot "<grep IOR ../dat/alcf_2-9_3-1.dat | grep MPIIO | grep read" using 9:($7/1024) with points pt 1 title "IOR-shared-read", \
     "<grep IOR ../dat/alcf_2-9_3-1.dat | grep POSIX | grep read" using 9:($7/1024) with points pt 2 title "IOR-fpp-read", \
     "<grep HACC-IO ../dat/alcf_2-9_3-1.dat | grep read" using 9:($7/1024) with points pt 3 title "HACC-fpp-read", \
     "<grep BD-CATS-IO ../dat/alcf_2-9_3-1.dat" using 9:($7/1024) with points pt 4 title "VPIC-shared-read"

set output "edison-scratch1-write-perf.eps"

set yrange[0:45]

set xrange [1487052000:1488434400]
set xtics 1487052000,259200,1488434400 rotate by -45

plot "<grep IOR ../dat/nersc_2-14_3-1.dat | grep MPIIO | grep write | grep scratch1" using 9:($7/1024) with points pt 1 title "IOR-shared-write", \
     "<grep IOR ../dat/nersc_2-14_3-1.dat | grep POSIX | grep write | grep scratch1" using 9:($7/1024) with points pt 2 title "IOR-fpp-write", \
     "<grep HACC-IO ../dat/nersc_2-14_3-1.dat | grep write | grep scratch1" using 9:($7/1024) with points pt 3 title "HACC-fpp-write", \
     "<grep VPIC-IO ../dat/nersc_2-14_3-1.dat | grep scratch1" using 9:($7/1024) with points pt 4 title "VPIC-shared-write"

set output "edison-scratch1-read-perf.eps"

plot "<grep IOR ../dat/nersc_2-14_3-1.dat | grep MPIIO | grep read | grep scratch1" using 9:($7/1024) with points pt 1 title "IOR-shared-read", \
     "<grep IOR ../dat/nersc_2-14_3-1.dat | grep POSIX | grep read | grep scratch1" using 9:($7/1024) with points pt 2 title "IOR-fpp-read", \
     "<grep HACC-IO ../dat/nersc_2-14_3-1.dat | grep read | grep scratch1" using 9:($7/1024) with points pt 3 title "HACC-fpp-read", \
     "<grep BD-CATS-IO ../dat/nersc_2-14_3-1.dat | grep scratch1" using 9:($7/1024) with points pt 4 title "VPIC-shared-read"
