# sudo -u postgres createuser -s $USER # This will be needed only if not using Docker
# createdb $USER

# Pull the latest prostgresql
docker pull postgres


# Run docker image with mapping the database into local data at /var/lib/postgresql/data
docker run -d -v odoo-db:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres

# Needed to run odoo setup.py
sudo apt install libxml2-dev
sudo apt install libxslt-dev

docker exec -it db pg_config




sudo apt install python3-dev  # Fixes issues with installing gevent
sudo apt install libpq-dev  # Fixes issues with installing psycopg2
sudo apt-get install libldap2-dev  # Fixes issues with installing python-ldap
sudo apt-get install libsasl2-dev  # Fixes issues with installing gevent
pip install greenlet==2.0.0a2  # Fixes issues with installing greenlet
sudo apt install python-greenlet-dev  # Fixes issues with installing gevent
pip install -r ./requirements.txt
pip uninstall psycopg2  # replace psycopg2 with psycopg2-binary
pip install psycopg2-binary

sudo mkdir /var/run/postgresql
docker-compose -f ./docker-compose.yml up

docker exec -it odoo_odoo-db_1 bash
createdb -U odoo estate_test  # Create database "estate_test"
psql -h localhost -U odoo  # Open interactive psql shell

psql -h localhost -d estate_test -U odoo  # Open interactive psql shell with database estate_test
\l  # list running databases (one was created on odoo setup page)
\c estate_test  # switch to a database test0
\dt  # show tables in the database

1. Login, Pass: admin, admin
2. Activate Discuss module (or any module)
3. Settings -> General settings -> Enable developer mode
4. Install wkhtmltopdf (to send pdf in emails and for printing) on the host system