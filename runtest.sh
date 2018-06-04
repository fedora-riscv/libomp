#!/bin/bash

usage() {
    echo "usage: `basename $0` [OPTIONS]"
    echo "  --threads NUM       The number of threads to use for running tests."
}


threads_arg=''

while [ $# -gt 0 ]; do
    case $1 in
	--threads)
            shift
            threads_arg="--threads $1"
            ;;
        * )
            echo "unknown option: $1"
            echo ""
            usage
            exit 1
            ;;
    esac
    shift
done


set -x

lit $threads_arg -v --config-prefix clang /usr/share/libomp/src/runtime/test
fail=$?
lit $threads_arg -v --config-prefix gcc /usr/share/libomp/src/runtime/test
exit $fail || $?
