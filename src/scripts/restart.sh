#!/bin/bash

# restart chess script

# kill the process
while true
do
	PIDS="$(/bin/ps -C gunicorn -o pid=)"
	echo ${PIDS}	
	sudo kill ${PIDS}

	# restart the process
	cd /home/ubuntu/chess-engine-with-ai/
	source venv/bin/activate
	cd src/
	nohup gunicorn wsgi &
	sleep 3000
done
