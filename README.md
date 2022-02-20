# gcd-django-docker

This uses Docker and Docker Compose, which need to be installed first.

After cloning this repo into a directory, follow these steps:

1. build images - `docker-compose build`
1. start services in detached mode, or not use -d to see the logs - `docker-compose up -d`
1. run migrations - `docker-compose run web /usr/local/bin/python gcd-django/manage.py migrate`

This will result in a running website without any data.

To import data, login to the GCD and download a (current) dump from https://www.comics.org/download/.

After unzipping the dump, run the following with the name of the 'current_dump':  
`docker exec -i gcd-django-docker_db_1 mysql -u gcd-django my-gcd-db -p'db-gcd' < 'current_dump'`

Do load users into the system, use  
`docker-compose run web python gcd-django/manage.py loaddata gcd-django/apps/indexer/fixtures/users.yaml`  
The three development users are (passwords in ()): `admin (admin)`, `editor (editme)`, and `dexter_1234 (test)`.

This get a shell use `docker exec -it gcd-django-docker_web_1 bash`, e.g. to locally edit files. After changing into `gcd-django` you can get a django shell with `python manage.py shell`.
