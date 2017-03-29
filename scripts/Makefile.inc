SED ?= sed
%.py: %.ipynb
	( ipython nbconvert --to python $< && \
    chmod +x $@; \
    $(SED) -i '1s~^~#!/usr/bin/env python~' $@; \
    $(SED) -i '/^ *get_ipython/d' $@; \
    $(SED) -ri 's/^( *import matplotlib *)$$/\1\nmatplotlib.use("Agg")/' $@; \
    $(SED) -i '/^# In\[[0-9 ]*\]: *$$/d' $@ )
