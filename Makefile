PDFS := holistic-io.pdf

all: $(PDFS)

holistic-io.pdf: holistic-io.tex REFERENCES.bib
	pdflatex $<
	bibtex holistic-io
	pdflatex $<
	pdflatex $<

clean::
	rm -f $(PDFS) *.dvi *.aux *.bbl *.log *.bak *.toc *.blg *.lof *.ps
