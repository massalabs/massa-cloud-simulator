#!/bin/sh
sleep 60
  
>&2 echo "Executing Sleep Command"
# Print and execute all other arguments starting with `$1`
# So `exec "$1" "$2" "$3" ...`
exec "$@"
