#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "{database_name}" ]; then
  echo "Waiting for {database_name}..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$MONGO_DATABASE" = "{mongo_database_name}" ]; then
  echo "Waiting for {mongo_database_name}..."

  while ! nc -z $MONGO_HOST $MONGO_PORT; do
    sleep 0.1
  done

  echo "MongoDB started"
fi

while ! nc -z zookeeper 2181; do
  sleep 0.1
done
echo "Kafka started"

manage init
manage load

gunicorn --bind 0.0.0.0:5000 manage:app
