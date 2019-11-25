#!/bin/bash
set -e

if [ "$1" = 'testsuite' ]; then
    exec pytest --capture=no tests
fi

su django -c "python /web/manage.py migrate"
exec uwsgi --ini uwsgi.ini "$@"
