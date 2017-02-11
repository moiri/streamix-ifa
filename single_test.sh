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
-j TOPOLOGY         only test the specified json topology
-a AUTOMATA         only test the specified automata type
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
YELLOW='\033[0;33m'
NC='\033[0m'
f="gml"
ds="False"
db="False"
flags="-b"
j=""
a=""
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
            flags="-p $flags"
            ;;
        -v)
            v=true
            ;;
        -j)
            j="$2"
            shift
            ;;
        -a)
            a="$2"
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
        ja[0]="-j circle"
        ja[1]="-j linear"
    else
        ja[0]="-j $j"
    fi
fi

if [ -z "$a" ]; then
    aa[0]="sync"
    aa[1]="buf"
else
    aa[0]="$a"
fi

failed="${RED}failed${NC} "
success="${GREEN}success${NC}"
for j in "${ja[@]}"
do
    for a in "${aa[@]}"
    do
        if [ "$a" == "sync" ] ; then
            res=$ds
        elif [ "$a" == "buf" ] ; then
            res=$db
        fi
        cmd="./ifa.py $flags $j -f $f -a $a $infile"
        if [ "$v" = true ] ; then
            echo "testing: $cmd"
        fi
        out="$( $cmd 2>&1 > /dev/null )"
        out_pr=${LGREY}[dl=${out//True/True }]${NC}
        if [ "$out" == "$res" ]; then
            if [ "$v" = true ] ; then
                echo -e " => $success $out_pr"
            fi
        else
            if [ "$v" = false ] ; then
                echo -e "$failed $out_pr: $cmd"
                echo -e " => ${YELLOW}expected '$res' got '$out'${NC}"
            else
                echo -e " => $failed $out_pr, ${YELLOW}expected '$res'${NC}"
            fi
        fi
    done
done
