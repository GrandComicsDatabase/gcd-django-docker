# gcd-django-docker

This uses Docker and Docker Compose, which need to be installed first.

After cloning this repo into a directory, and editing the ports if needed, follow these steps:

1. build images - `docker-compose build`
1. start services, or use -d in detached mode to see the logs - `docker-compose up`
1. run migrations - `docker-compose run web /usr/local/bin/python gcd-django/manage.py migrate`

On the first run the mysql-setup needs time, it needs to finish to have the db present before you can run migrate. The migrate also takes quite some minutes.

This will result in a running website without any data.
Check the names of your containers with `docker-compose images`, one is for the db-server (use that as 'db_container_name') and one is for the website-server (use that as 'web_container_name').

To import data, login to the GCD and download a (current) dump from https://www.comics.org/download/.

After unzipping the dump, run the following with the name of the 'current_dump':  
`docker exec -i 'db_container_name' mysql -u gcd-django my-gcd-db -p'db-gcd' < 'current_dump'`

To view the website, access http://0.0.0.0:8000/.

To load users into the system, first run the migrations again:  
 `docker-compose run web /usr/local/bin/python gcd-django/manage.py migrate`
(note that we currently don't know why the migration needs to be done again) and then use  
`docker-compose run web python gcd-django/manage.py loaddata gcd-django/apps/indexer/fixtures/users.yaml`  
The three development users are (passwords in ()): `admin (admin)`, `editor (editme)`, and `dexter_1234 (test)`.

To get a shell use `docker exec -it 'web_container_name' bash`, e.g. to locally edit files. After changing into `gcd-django` you can get a django shell with `python manage.py shell`.

If doing development work on the code for editing, note that right now you cannot edit existing data, since we do not export the change history in the dump. But, you can add new data (with dexter_1234), approve it (with editor), and then edit the newly added data. We intend to add a changesets for the existing data to allow their editing in this development setup.

To allow approvals to work, the statistics need to exist, for that run the following:  
`docker-compose run web python gcd-django/manage.py runscript reset_stats`

This setup so far does not support elasticsearch, i.e., the regular search. For that we likely need two more containers, one for elasticsearch, and (maybe) one for reddis.
