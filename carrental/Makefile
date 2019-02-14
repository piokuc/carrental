recreatedb:
	rm -f db.sqlite3
	python manage.py migrate --run-syncdb
	python manage.py createsuperuser

test:
	python manage.py test

run:
	python manage.py runserver

shell:
	python manage.py shell
