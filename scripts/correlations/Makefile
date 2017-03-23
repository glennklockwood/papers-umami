.PHONY: clean default

targets=correlation_analysis.py

all: $(targets)

%.py: %.ipynb
	( ipython nbconvert --to python $< && \
    chmod +x $@; \
    sed -i '1s~^~#!/usr/bin/env python~' $@; \
    sed -i '/^ *get_ipython/d' $@; \
    sed -ri 's/^( *import matplotlib *)$$/\1\nmatplotlib.use("Agg")/' $@ )

clean:
	rm -f $(targets)
