#!/bin/sh

create_superuser_if_not_exists() {
    # 检查是否存在超级用户
    SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())")

    if [ "$SUPERUSER_EXISTS" = "False" ]; then
        echo "No superuser exists. Creating one..."
        python manage.py createsuperuser --noinput
    else
        echo "Superuser already exists."
    fi
}

python manage.py makemigrations api && \
python manage.py migrate && \
create_superuser_if_not_exists && \
python manage.py loaddata initial_data.json && \
python manage.py collectstatic --noinput && \
nginx && gunicorn --bind 0.0.0.0:8000 reviveit_backend.wsgi:application