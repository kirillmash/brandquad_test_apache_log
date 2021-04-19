import os
from datetime import datetime

import apache_log_parser

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator

import requests

from apache_log.models import Log


class Command(BaseCommand):
    help = 'Download apache log and database entry'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']
        validate = URLValidator()
        try:
            validate(url)
        except ValidationError:
            raise CommandError('Invalid url')
        r = requests.get(url, allow_redirects=True)
        file_name = f"{datetime.now().strftime('%d_%m_%Y_%H%M%S')}_{url.split('/')[-1]}"
        path = os.path.abspath(os.path.join('apache_log', 'logs', file_name))
        open(path, 'wb').write(r.content)

        log_to_db = []
        pattern_to_parser = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
        line_parser = apache_log_parser.make_parser(pattern_to_parser)
        with open(path, 'r') as f:
            for line in f:
                if not line == '\n':
                    log_line = line_parser(line)
                    log_to_db.append(Log(
                        ip=log_line['remote_host'],
                        date_log=log_line['time_received_utc_datetimeobj'],
                        http_method=log_line['request_method'],
                        url=log_line['request_url'],
                        status_response=log_line['status'],
                        size_response=log_line['response_bytes_clf'],
                        user_agent=log_line['request_header_user_agent']
                    ))
        Log.objects.bulk_create(log_to_db)
        self.stdout.write(self.style.SUCCESS('Successful'))

