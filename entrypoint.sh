#!/bin/bash
if [ ! -z "$PSQL_PASS_FILE" -a -z "$PASSWORD" ]
then
         PASSWORD=$(cat $PSQL_PASS_FILE)
fi
set -e
#sed -i "s/DATABASE_HOST/$DATABASE_HOST/g" /opt/engine/config.json
#sed -i "s/DATABASE_PORT/$DATABASE_PORT/g" /opt/engine/config.json
#sed -i "s/POSTGRESHARMONY_HOST/$POSTGRESHARMONY_HOST/g" /opt/engine/config.json
#sed -i "s/REDIS_HOST/$REDIS_HOST/g" /opt/engine/config.json
#sed -i "s/REDIS_PORT/$REDIS_PORT/g" /opt/engine/config.json
#sed -i "s/DATABASE/$DATABASE/g" /opt/engine/config.json
#sed -i "s/USERNAME/$USERNAME/g" /opt/engine/config.json
#sed -i "s/PASSWORD/$PASSWORD/g" /opt/engine/config.json
#sed -i "s/RUN_PORT/$PORT/g" /engine/config.json

echo "Starting Flask file"
sh /engine/flask.sh &