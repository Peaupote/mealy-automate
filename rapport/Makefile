LATEX = pdflatex
BIB = bibtex

rapport: project.tex project.bib
	@echo "Compiling latex report"
	@$(LATEX) project
	@$(BIB)   project
	@$(LATEX) project
