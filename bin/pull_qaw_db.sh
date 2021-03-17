#!/bin/bash

ssh -i /home/dallanbhatti/.ssh/github super_dallan@mega <<EOF
  docker exec league_db pg_dump -c -U "$1" league > league.sql
EOF
rsync -chavzP --stats --remove-source-files super_dallan@mega:/home/super_dallan/league.sql "$HUNCHO_DIR"/services/league/league.sql

docker exec -i league_db psql -U "$1" league <"$HUNCHO_DIR"/services/league/league.sql
