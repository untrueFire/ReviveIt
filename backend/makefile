dev:
	./manage.py runserver
test:
	coverage run --include=api/*.py ./manage.py test --settings=test_setting
lint:
	uv run pylint --rcfile=.pylintrc api reviveit_backend
init:
	./manage.py makemigrations api && \
	./manage.py migrate && \
	./manage.py createsuperuser
