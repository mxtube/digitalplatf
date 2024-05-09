#!/bin/bash -eu

DOCKER_RUN="docker run --rm --env-file=.env
  -e POSTGRES_HOST=${DB_HOST:-host.docker.interval} -e POSTGRES_PORT -e POSTGRES_DB -e POSTGRES_USER -e POSTGRES_PASSWORD"

if [[ $# -eq 0 ]]; then
  echo "Usage: ./run.sh <service>"
  echo "Select service:"
  grep -E '^\s+\w{3}\S+\)' "$0" | awk -F '[\|\)]' '{ print $2 "\t" $1; }'
  exit 1
fi

SERVICE="${1:-}"
shift

case "$SERVICE" in

  # Запуск сервера Django
  web_server|1)
    pushd src
    PYTHONPATH="${PWD}:${PWD}/src" python3 manage.py runserver "$@"
  ;;

  # Миграция базы данных
  pg_migrate|2)
    pushd src
    PYTHONPATH="${PWD}:${PWD}/src" python3 manage.py migrate "$@"
  ;;

  # Импорт тестовых данных в базу
  generate_test_data|3)
    pushd src
    "${PWD}/migrate_db.sh" "$@"
  ;;

  # PostgreSQL в Docker
  pg_docker|4)
    docker run -d \
      --name ${POSTGRES_CONTAINER_NAME:-dp_psql} \
      -p ${POSTGRES_PORT:-5432}:5432 \
      -e POSTGRES_DB=${POSTGRES_DB:-dev_dp} \
      -e POSTGRES_USER=${POSTGRES_USER:-psqldp} \
      -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-Gthtgjkj12} \
      postgres:16.2 "$@"
  ;;

  # Redis в Docker
  rd_docker|5)
    $DOCKER_RUN --name ${REDIS_CONTAINER_NAME:-dp_redis} -d -p ${REDIS_PORT:-6379}:6379 \
     -e REDIS_PASSWORD=${REDIS_PASSWORD:-Gthtgjkj12} \
     redis:7.2.4 "$@"
  ;;

  # Запустить Celery
  celery|6)
    pushd src
    PYTHONPATH="${PWD}:${PWD}/src" celery -A core worker -l INFO "$@"
  ;;

  # Очистить data
  clear_data|6)
    pushd data
    rm -R * "$@"
  ;;
esac



#celery -A core worker -l INFO --detach
#./manage.py runserver