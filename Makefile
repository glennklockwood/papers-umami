PDFS := holistic-io.pdf

all: $(PDFS)

SECTIONS=abstract.tex introduction.tex methods.tex results.tex related.tex appendix.tex appendix-analysis.tex appendix-artifacts.tex

holistic-io.pdf: holistic-io.tex REFERENCES.bib $(SECTIONS)
	pdflatex $<
	bibtex holistic-io
	pdflatex $<
	pdflatex $<

clean::
	rm -f $(PDFS) *.dvi *.aux *.bbl *.log *.bak *.toc *.blg *.lof *.ps
