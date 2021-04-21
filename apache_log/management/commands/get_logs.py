import apache_log_parser

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator

import requests

from apache_log.models import Log


MAX_ROWS = 999

CHUNK_SIZE = 1024 * 100


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
        r = requests.get(url, stream=True)
        if not r.ok:
            raise CommandError(f"Server status - {r.status_code}")
        pattern_to_parser = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
        line_parser = apache_log_parser.make_parser(pattern_to_parser)
        counter = 0
        log_to_db = []
        for line in r.iter_lines(chunk_size=CHUNK_SIZE):
            if line:
                decode_line = line.decode('utf-8')
                try:
                    log_line = line_parser(decode_line)
                    log_to_db.append(Log(ip=log_line['remote_host'],
                                         date_log=log_line['time_received_utc_datetimeobj'],
                                         http_method=log_line['request_method'],
                                         url=log_line['request_url'],
                                         status_response=log_line['status'],
                                         size_response=log_line['response_bytes_clf'],
                                         user_agent=log_line['request_header_user_agent']))
                except apache_log_parser.LineDoesntMatchException:
                    continue
                counter += 1
                if counter == MAX_ROWS:
                    Log.objects.bulk_create(log_to_db)
                    counter = 0
                    log_to_db = []
        if log_to_db:
            Log.objects.bulk_create(log_to_db)
        self.stdout.write(self.style.SUCCESS('Successful'))
