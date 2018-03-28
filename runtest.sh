#!/bin/bash

set -x

lit -v --config-prefix clang /usr/share/libomp/src/runtime/test
fail=$?
lit -v --config-prefix gcc /usr/share/libomp/src/runtime/test
exit $fail || $?
