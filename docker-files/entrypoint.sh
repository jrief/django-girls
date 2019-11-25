#!/bin/bash
set -e

if [ "X$1" == "Xtestsuite" ]; then
	exec pytest --capture=no tests
fi

manage_migrate() {
	su django -c "python /web/manage.py migrate"
}

if [ "X$1" == "Xuwsgi" ]; then
	manage_migrate
	exec "$@" --ini uwsgi.ini
elif [ "X$1" == "X" ]; then
	manage_migrate
	exec uwsgi --ini uwsgi.ini
else
	exec "$@"
fi
