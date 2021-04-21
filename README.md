# brandquad test_apache_log
parse apache log




# Run application

1. With docker: `docker-compose up` (docker should be installed)

Application will be available at http://127.0.0.1:8000

2. Download and parse log `docker-compose exec web python manage.py get_logs URL`

Example:
`docker-compose exec web python manage.py get_logs http://www.almhuette-raith.at/apache-log/access.log`

3. Create superuser: `docker-compose exec web python manage.py createsuperuser`

4. Logs will be shown at http://127.0.0.1:8000/admin


## Challenge:

![image](https://user-images.githubusercontent.com/74962029/115206119-f063a200-a102-11eb-8757-3d1ddb10a551.png)
