#!/bin/sh

document="${1%.*}"

[ -d ./aux ] || mkdir ./aux
[ -d ./out ] || mkdir ./out


_pdflatex() {
    echo "pdflatex - $1"
    pdflatex-dev \
        -synctex=1 \
        -output-directory=./aux \
        -halt-on-error \
        "$document.tex" 1>>"./out/$1.out"
    status=$?
    [ $status -eq 0 ] || _error
}

_biber() {
    echo "biber - $1"
    biber \
        "./aux/$document" 1>>"./out/$1.out"
    status=$?
    [ $status -eq 0 ] || _error
}

_error() {
    if [ -f "./aux/$document.log" ]; then
        cp "./aux/$document.log" . &&
        echo "Error occured - check '$document.log' and 'out/' for details" &&
        _cleanup
    else
        echo "Error occured, no log file is available" &&
        _cleanup
    fi
    exit 1
}

_postprocessing() {
    cp "./aux/$document.pdf" .
    cp "./aux/$document.log" .
    _cleanup
}

_setup() {
    rm -r ./out/*
}

_cleanup() {
    rm -r ./aux
}

_setup
_pdflatex "Generating document"
_biber "Generating references"
_pdflatex "Attaching references"
_pdflatex "Enumerating references"
_postprocessing 