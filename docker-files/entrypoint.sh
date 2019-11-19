#!/bin/bash
set -e

if [ "$1" = 'testsuite' ]; then
    exec pytest --capture=no tests
fi

exec "$@"
