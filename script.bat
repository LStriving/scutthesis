del *.aux *.lo? *.toc *.ind *.inx *.gls *.glo *.ist *.idx *.ilg *.out *.bak *.bbl *.brf *.blg *.dvi *.ps *.xdv sec\*.aux
del main.pdf 2>nul
xelatex -no-pdf -shell-escape --interaction=nonstopmode main
bibtex main 
bibtex main 
xelatex -no-pdf -shell-escape --interaction=nonstopmode main 
xelatex -shell-escape --interaction=nonstopmode main 
code main.pdf