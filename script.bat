@echo off
setlocal

set "MAIN=main"
set "OUTDIR=build"

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

del /q "%MAIN%.pdf" 2>nul

python dedup_bib.py --input "%MAIN%.bib"
if errorlevel 1 goto :end

xelatex -no-pdf -shell-escape --interaction=nonstopmode -output-directory="%OUTDIR%" "%MAIN%.tex"
if errorlevel 1 goto :end

pushd "%OUTDIR%"
set "BIBINPUTS=.;..;"
set "BSTINPUTS=.;..;"
bibtex "%MAIN%"
popd
if errorlevel 1 goto :end

xelatex -no-pdf -shell-escape --interaction=nonstopmode -output-directory="%OUTDIR%" "%MAIN%.tex"
if errorlevel 1 goto :end

xelatex -shell-escape --interaction=nonstopmode -output-directory="%OUTDIR%" "%MAIN%.tex"
if errorlevel 1 goto :end

copy /y "%OUTDIR%\%MAIN%.pdf" "%MAIN%.pdf" >nul
start "" "%MAIN%.pdf"

:end
endlocal