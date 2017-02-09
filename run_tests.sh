#!/bin/sh
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
-v                  verbose

EOF

    exit 1
}

v=""
while [ $# -gt 0 ] ; do
    case "$1" in
        -h|--help)
            usage
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

./single_test.sh $v -f json -j circle ./test/serial1.json
./single_test.sh $v -f json -j circle ./test/serial2.json
./single_test.sh $v -f json -j circle -ds ./test/serial3.json
./single_test.sh $v -f gml -ds ./test/serial4_1.gml ./test/serial4_2.gml
./single_test.sh $v -f gml -ds ./test/serial4b_1.gml ./test/serial4_2.gml
./single_test.sh $v -f gml -ds ./test/serial4c_1.gml ./test/serial4_2.gml
./single_test.sh $v -f gml -ds ./test/serial4c_1.gml ./test/serial4_2.gml ./test/serial4c_3.gml
./single_test.sh $v -f json -j circle ./test/feedback1.json
./single_test.sh $v -f json -j circle -ds ./test/feedback2.json
./single_test.sh $v -f json -j circle -ds -db ./test/feedback3.json
./single_test.sh $v -f gml -ds ./test/feedback4_1.gml ./test/feedback4_2.gml
./single_test.sh $v -f gml -ds ./test/feedback4b_1.gml ./test/feedback4_2.gml
./single_test.sh $v -f gml -ds ./test/feedback4c_1.gml ./test/feedback4_2.gml ./test/serial4c_3.gml
./single_test.sh $v -f gml -ds -db ./test/feedback5_1.gml ./test/feedback5_2.gml
./single_test.sh $v -f gml -ds -db ./test/feedback5b_1.gml ./test/feedback5_2.gml
./single_test.sh $v -f gml -ds -db ./test/feedback5c_1.gml ./test/feedback5_2.gml ./test/serial4c_3.gml
./single_test.sh $v -f json -j circle ./test/feedback6.json
./single_test.sh $v -f json -j circle -ds -db ./test/feedback7.json
./single_test.sh $v -f json -j circle ./test/loop1.json
./single_test.sh $v -f json -j circle -ds ./test/loop2.json
