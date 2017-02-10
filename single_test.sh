#!/bin/bash
#http://agateau.com/2014/template-for-shell-based-command-line-scripts/
set -e

PROGNAME=$(basename $0)

die() {
    echo "$PROGNAME: $*" >&2
    exit 1
}

usage() {
    if [ "$*" != "" ] ; then
        echo "Error: $*"
    fi

    cat << EOF

Usage: $PROGNAME [OPTION ...] infile_1 [infile_2] ... [infile_n]

Run the ifa script and compare the output to a sulution file

Options:
-h, --help          display this usage message and exit
-f FORMAT           set the format of the input graph (default: gml)
-p                  print final graph
-v                  verbose
-ds                 if set sync is deadlocking
-db                 if set buffer is deadlocking

EOF

    exit 1
}

RED='\033[0;31m'
GREEN='\033[0;32m'
LGREY='\033[0;90m'
NC='\033[0m'
f="gml"
ds="False"
db="False"
p=""
j=""
v=false
infile=""
while [ $# -gt 0 ] ; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -ds)
            ds="True"
            ;;
        -db)
            db="True"
            ;;
        -p)
            p=" -p"
            ;;
        -v)
            v=true
            ;;
        -j)
            j="$2"
            shift
            ;;
        -f)
            f="$2"
            shift
            ;;
        -*)
            usage "Unknown option '$1'"
            ;;
        *)
            infile="$infile$1 "
            ;;
    esac
    shift
done

if [ -z "$infile" ] ; then
    usage "Not enough arguments"
fi

if [ "$f" == "gml" ]; then
    ja[0]=""
elif [ "$f" == "json" ]; then
    if [ -z "$j" ] ; then
        ja[0]=" -j circle"
        ja[1]=" -j linear"
    else
        ja[0]=" -j $j"
    fi
fi

failed="${RED}failed${NC} "
success="${GREEN}success${NC}"
for j in "${ja[@]}"
do
    cmd="./ifa.py -b$p -f $f$j -a sync $infile"
    out="$($cmd)"
    out_pr=${LGREY}[${out//True/True }]${NC}
    if [ "$out" == "$ds" ]; then
        if [ "$v" = true ] ; then
            echo -e "$success $out_pr: $cmd"
        fi
    else
        echo -e "$failed $out_pr: $cmd"
        echo -e "  => expected '$ds' got '$out'"
    fi

    cmd="./ifa.py -b$p -f $f$j -a buf $infile"
    out="$($cmd)"
    out_pr=${LGREY}[${out//True/True }]${NC}
    if [ "$out" == "$db" ]; then
        if [ "$v" = true ] ; then
            echo -e "$success $out_pr: $cmd"
        fi
    else
        echo -e "$failed $out_pr: $cmd"
        echo -e "  => expected '$db' got '$out'"
    fi
done
