.PHONY: clean default

targets=correlation_analysis.py

all: $(targets)

include ../Makefile.inc

clean:
	rm -vf $(targets)

clean-all: clean
	rm -vf *.pdf *.png scatter_*_vs_*.csv
