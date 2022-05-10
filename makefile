setup:
	pip install -r requirements.txt
	python3 manage.py tailwind install
	python3 manage.py makemigrations
	python3 manage.py migrate
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py builddb
run:
	python3 manage.py runserver
tailwind:
	python3 manage.py tailwind start
setuph:
	pip install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate