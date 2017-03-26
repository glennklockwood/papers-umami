#!/usr/bin/env bash
#
#  Figure out which figures we actually need to keep from the .tex files
#  themselves.
#

grep -Eo 'figs[^{]*.(png|pdf|jpeg)' *.tex
