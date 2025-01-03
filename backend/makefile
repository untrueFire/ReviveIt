dev:
	./manage.py runserver
test:
	coverage run --include=api/*.py ./manage.py test --settings=test_setting
lint:
	uv run pylint --rcfile=.pylintrc api reviveit_backend
init:
	cp static/default_avatar.png files/b601fca160d2d48dd2a5b16c046433c9ca9dda5940941ad58431341d654f6bc9.png && \
	./manage.py makemigrations api && \
	./manage.py migrate && \
	./manage.py createsuperuser && \
	./manage.py loaddata api/fixtures/initial_data.json
sync:
	./manage.py makemigrations api && \
	./manage.py migrate