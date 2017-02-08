set term po eps color dashed 16 size 5in,2.33in

# color blindness work around
set style line 1 lc 1 lw 2 ps 0.5
set style line 2 lc 3 lw 2 ps 0.5
set style line 3 lc 4 lw 2 ps 0.5
set style line 4 lc 5 lw 2
set style line 5 lc 2 lw 2
set style increment user

set output "example-bar-var.eps"
set grid ytics
set key outside
#set key top right
#set xlabel "Access size (bytes)" offset -2,1
#set ylabel "Latency (us)" offset 3,-2
#set grid
#set rmargin 2

#set logscale x
#set logscale y
set yrange [0:]
set xtic nomirror rotate by -45
#set rmargin 4
#set lmargin 6
#set bmargin 8

#set yrange [1:10000000]

set style data histogram
set style histogram errorbars gap 1

set style fill solid border rgb "black"
set auto x
set xlabel "System"
set ylabel "(normalized bandwidth or execution time?)"
plot 'example-bar-var.dat' using ($3):($2):($4):xtic(1) title col, \
    '' using ($6):($5):($7):xtic(1) title col, \
    '' using ($9):($8):($10):xtic(1) title col, \
    '' using ($12):($11):($13):xtic(1) title col

#plot "<(grep write latency-paper.output)" using 3:($6*(1000*1000)) with linespoints lt 1 pt 7 linecolor rgb "red" title "write", \
#"<(grep read latency-paper.output)" using 3:($6*(1000*1000)) with linespoints lt 1 pt 7 linecolor rgb "green" title "read"

