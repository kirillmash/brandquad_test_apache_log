# brandquad_test_apache_log
parse apache log




# Run application

1. With docker: `docker-compose up` (docker should be installed)

Application will be available at http://127.0.0.1:8000

2. Download and parse log `docker-compose exec web python manage.py get_logs URL`

Example:
`docker-compose exec web python manage.py get_logs http://www.almhuette-raith.at/apache-log/access.log`

3. Create superuser: `docker-compose exec web python manage.py createsuperuser`

4. Logs will be shown at http://127.0.0.1:8000/admin
