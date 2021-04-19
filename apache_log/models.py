from django.db import models


class Log(models.Model):
    ip = models.GenericIPAddressField()
    date_log = models.DateField()
    http_method = models.CharField(max_length=16)
    url = models.CharField(max_length=255)
    status_response = models.IntegerField()
    size_response = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
