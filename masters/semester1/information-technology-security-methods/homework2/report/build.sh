#!/bin/sh

document="${1%.*}"

[ -d ./aux ] || mkdir ./aux


_pdflatex() {
    echo "pdflatex - $1"
    pdflatex-dev \
        -synctex=1 \
        -output-directory=./aux \
        -halt-on-error \
        "$document.tex" 1>/dev/null
    status=$?
    [ $status -eq 0 ] || _error
}

_biber() {
    echo "biber - $1"
    biber \
        "./aux/$document" 1>/dev/null
    status=$?
    [ $status -eq 0 ] || _error
}

_error() {
    if [ -f "./aux/$document.log" ]; then
        cp "./aux/$document.log" . &&
        echo "Error occured - check '$document.log' for details" &&
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

_cleanup() {
    rm -r ./aux
}

_pdflatex "Generating document"
_biber "Generating references"
_pdflatex "Attaching references"
_pdflatex "Enumerating references"
_postprocessing 