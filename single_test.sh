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
-j TOPO             set the topology of json input graph (default: circle)
-v                  verbose
-ds                 if set sync is deadlocking
-db                 if set buffer is deadlocking

EOF

    exit 1
}

f="gml"
j="circle"
ds="False"
db="False"
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
        -v)
            v=true
            ;;
        -f)
            f="$2"
            shift
            ;;
        -j)
            j="$2"
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

cmd="./ifa.py -b -f $f -j $j -a sync -d eps $infile"
out="$($cmd)"
if [ "$out" == "$ds" ]; then
    if [ "$v" = true ] ; then
        echo $cmd
        echo "  => success"
    fi
else
    echo $cmd
    echo "  => failed: expected '$ds' got '$out'"
fi

cmd="./ifa.py -b -f $f -j $j -a sync -d vdl $infile"
out="$($cmd)"
if [ "$out" == "$ds" ]; then
    if [ "$v" = true ] ; then
        echo $cmd
        echo "  => success"
    fi
else
    echo $cmd
    echo "  => failed: expected '$ds' got '$out'"
fi

cmd="./ifa.py -b -f $f -j $j -a buf -d eps $infile"
out="$($cmd)"
if [ "$out" == "$db" ]; then
    if [ "$v" = true ] ; then
        echo $cmd
        echo "  => success"
    fi
else
    echo $cmd
    echo "  => failed: expected '$db' got '$out'"
fi

cmd="./ifa.py -b -f $f -j $j -a buf -d vdl $infile"
out="$($cmd)"
if [ "$out" == "$db" ]; then
    if [ "$v" = true ] ; then
        echo $cmd
        echo "  => success"
    fi
else
    echo $cmd
    echo "  => failed: expected '$db' got '$out'"
fi

if [ "$v" = true ] ; then
    echo
fi
