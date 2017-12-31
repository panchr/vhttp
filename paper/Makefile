PAPER=vhttp
BIBTEX := bibtex
TGIF   := tgif
XFIG   := xfig
GNUPLOT:= gnuplot

SOURCES:=vhttp.tex \
	abstract.tex \
	intro.tex \
	design.tex \
	eval.tex \
	related.tex \
	conclusion.tex \
	references.bib

FIGURES:=$(wildcard figures/*.pdf figures/*.png figures/*.tex)

all: $(PAPER).pdf

$(PAPER).pdf: $(SOURCES) $(FIGURES)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)

# color: $(PAPER).pdf
# 	pdflatex $(PAPER).tex
# 	pdftops $(PAPER).pdf

# $(PAPER).ps: $(PAPER).pdf
# 	pdflatex "\newcommand{\wantBW}{} \input{$(PAPER).tex}"
# 	pdftops $(PAPER).pdf

%.pdf : %.fig #Makefile
	fig2dev -L pdf -b 1 $< $@

%.eps : %.dia #Makefile
	dia --nosplash -e $@ $<

%.eps : %.obj
	TMPDIR=/tmp $(TGIF) -print -eps $<

%.pdf : %.eps #Makefile
	epstopdf $<

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *~ *.bak $(FIGS) $(PAPER).ps $(PAPER).pdf
