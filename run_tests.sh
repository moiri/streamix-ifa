#!/bin/bash
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

Test a bunch of ifa scripts

Options:
-h, --help          display this usage message and exit
-t GROUP            only test specified group of test cases: 'serial',
                        'feedback', 'loop', 'parallel', 'mult'
-a AUTOMATA         only test specified automata type: 'sync', 'buf'
-p                  print final graph
-v                  verbose

EOF

    exit 1
}

v=""
p=""
t=""
a=""
while [ $# -gt 0 ] ; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -t)
            t="$2"
            shift
            ;;
        -a)
            a="$2"
            shift
            ;;
        -p)
            p="-p"
            ;;
        -v)
            v="-v"
            ;;
        -*)
            usage "Unknown option '$1'"
            ;;
    esac
    shift
done

if [ ! -z "$a" ]; then
    a="-a $a"
fi


if [ -z "$t" ] || [ "$t" == "serial" ]; then
    ./single_test.sh $v $p $a -f json ./test/serial1.json
    ./single_test.sh $v $p $a -f json ./test/serial2.json
    ./single_test.sh $v $p $a -f json -ds ./test/serial3.json
    ./single_test.sh $v $p $a -f gml -ds ./test/serial4_1.gml ./test/serial4_2.gml
    ./single_test.sh $v $p $a -f gml -ds ./test/serial4b_1.gml ./test/serial4_2.gml
    ./single_test.sh $v $p $a -f gml -ds ./test/serial4c_1.gml ./test/serial4_2.gml
    ./single_test.sh $v $p $a -f gml -ds ./test/serial4c_1.gml ./test/serial4_2.gml ./test/serial4c_3.gml
    ./single_test.sh $v $p $a -f json ./test/serial5.json
    ./single_test.sh $v $p $a -f json -ds ./test/serial6.json
    ./single_test.sh $v $p $a -f json -ds ./test/serial7.json
fi
if [ -z "$t" ] || [ "$t" == "feedback" ]; then
    ./single_test.sh $v $p $a -f json ./test/feedback1.json
    ./single_test.sh $v $p $a -f json -ds ./test/feedback2.json
    ./single_test.sh $v $p $a -f json -ds -db ./test/feedback3.json
    ./single_test.sh $v $p $a -f gml -ds ./test/feedback4_1.gml ./test/feedback4_2.gml
    ./single_test.sh $v $p $a -f gml -ds ./test/feedback4b_1.gml ./test/feedback4_2.gml
    ./single_test.sh $v $p $a -f gml -ds ./test/feedback4c_1.gml ./test/feedback4_2.gml ./test/serial4c_3.gml
    ./single_test.sh $v $p $a -f gml -ds -db ./test/feedback5_1.gml ./test/feedback5_2.gml
    ./single_test.sh $v $p $a -f gml -ds -db ./test/feedback5b_1.gml ./test/feedback5_2.gml
    ./single_test.sh $v $p $a -f gml -ds -db ./test/feedback5c_1.gml ./test/feedback5_2.gml ./test/serial4c_3.gml
    ./single_test.sh $v $p $a -f json ./test/feedback6.json
    ./single_test.sh $v $p $a -f json -ds -db ./test/feedback7.json
    ./single_test.sh $v $p $a -f json -ds ./test/feedback8.json
fi
if [ -z "$t" ] || [ "$t" == "loop" ]; then
    ./single_test.sh $v $p $a -f json ./test/loop1.json
    ./single_test.sh $v $p $a -f json -ds ./test/loop2.json
fi
if [ -z "$t" ] || [ "$t" == "parallel" ]; then
    ./single_test.sh $v $p $a -f json ./test/parallel1.json
    ./single_test.sh $v $p $a -f json ./test/parallel2.json
    ./single_test.sh $v $p $a -f json -ds ./test/parallel3.json
    ./single_test.sh $v $p $a -f json ./test/parallel4.json
    ./single_test.sh $v $p $a -f json -ds -db ./test/parallel5.json
    ./single_test.sh $v $p $a -f json -ds ./test/parallel6.json
    ./single_test.sh $v $p $a -f json -ds -db ./test/parallel7.json
    ./single_test.sh $v $p $a -f json ./test/parallel8.json
fi
if [ -z "$t" ] || [ "$t" == "mult" ]; then
    ./single_test.sh $v $p $a -f json ./test/mult1.json
    ./single_test.sh $v $p $a -f json -j circle ./test/mult2.json
    ./single_test.sh $v $p $a -f json -j linear -ds -db ./test/mult2.json
    ./single_test.sh $v $p $a -f json -j circle ./test/mult3.json
    ./single_test.sh $v $p $a -f json -j linear -ds -db ./test/mult3.json
    ./single_test.sh $v $p $a -f json -ds -db ./test/mult4.json
fi
