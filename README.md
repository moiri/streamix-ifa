# streamix-sia
Compatibility check of synchronous interface automata

Requires `python-igraph` package: `pip install python-igraph`

In order to install `pip` run

    sudo apt update
    sudo apt install python-pip

## Install

Run the following commands

    make
    sudo make install

This will install the package with `pip` and copy `check_sia.py` to `/usr/local/bin/smxsia`.

## Run Testcases with Unittest

    python -m unittest <name of test file, starting with `test_`>

## Usage
To check a system, run `check_sia.py`.

    usage: This script performs the folding operation on interface automata passed as graphml files
           [-h] [-f FORMAT] [-o OUTFILE] NET INFILE [INFILE ...]

    positional arguments:
      NET         the dependency graph of the PNSC
      INFILE      the graph files to be folded

    optional arguments:
      -h, --help  show this help message and exit
      -f FORMAT   set the format of the input graph (default: graphml)
      -o OUTFILE  set the output path of the result (default: out.[FORMAT])

