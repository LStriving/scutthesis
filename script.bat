del *.aux *.lo? *.toc *.ind *.inx *.gls *.glo *.ist *.idx *.ilg *.out *.bak *.bbl *.brf *.blg *.dvi *.ps *.xdv sec\*.aux
del main.pdf 
xelatex -no-pdf --interaction=nonstopmode main
bibtex main 
bibtex main 
xelatex -no-pdf --interaction=nonstopmode main 
xelatex --interaction=nonstopmode main 
