python manage.py migrate

if [ -z "${WEB_CONCURENCY}" ];
then
  export WEB_CONCURENCY=$(($(nproc) * 2 + 1))
fi

echo "WEB_CONCURENCY is '$WEB_CONCURENCY'";
gunicorn backend.wsgi:application -b 0.0.0.0:8000 --threads 2 --worker-class gthread
