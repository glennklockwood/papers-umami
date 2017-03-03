set term po eps color dashed 16 size 4in,3in

# color blindness work around
set style line 1 lc 1 lw 2 ps 0.5
set style line 2 lc 3 lw 2 ps 0.5
set style line 3 lc 4 lw 2 ps 0.5
set style line 4 lc 5 lw 2
set style line 5 lc 2 lw 2
set style increment user

set output "tokio-abc-write-fingerprints.eps"

set key out right center

#set xrange [0:3]
#set xtics ("mira" 1, "edison" 2)
set xtic nomirror rotate by -45
set xtic scale 0
set xtics offset -.5

set ylabel "Bandwidth (normalized to max. for each system)"
set yrange [0:1]
set grid ytics

set style fill solid 1.00 border 0
set style data histogram
set style histogram cluster errorbars lw 1

plot "<grep IOR io-fingerprint-dat/write-perf-stats.dat | grep MPIIO" using 9:7:8:xtic(1) title "IOR (shared)", \
     "<grep IOR io-fingerprint-dat/write-perf-stats.dat | grep POSIX" using 9:7:8:xtic(1) title "IOR (fpp)", \
     "<grep HACC-IO io-fingerprint-dat/write-perf-stats.dat" using 9:7:8:xtic(1) title "HACC-IO (fpp)", \
     "<grep VPIC-IO io-fingerprint-dat/write-perf-stats.dat" using 9:7:8:xtic(1) title "VPIC-IO (shared)"
    
set output "tokio-abc-read-fingerprints.eps"

plot "<grep IOR io-fingerprint-dat/read-perf-stats.dat | grep MPIIO" using 9:7:8:xtic(1) title "IOR (shared)", \
     "<grep IOR io-fingerprint-dat/read-perf-stats.dat | grep POSIX" using 9:7:8:xtic(1) title "IOR (fpp)", \
     "<grep HACC-IO io-fingerprint-dat/read-perf-stats.dat" using 9:7:8:xtic(1) title "HACC-IO (fpp)", \
     "<grep BD-CATS-IO io-fingerprint-dat/read-perf-stats.dat" using 9:7:8:xtic(1) title "BD-CATS-IO (shared)"
