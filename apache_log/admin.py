from django.contrib import admin

from apache_log.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'date_log', 'http_method', 'url', 'status_response', 'size_response', 'user_agent')
    list_display_links = ('id', 'ip',)
    fields = ('ip', 'date_log', 'http_method', 'url', 'status_response', 'size_response', 'user_agent')
    search_fields = ('id', 'ip', )
    list_filter = ('http_method', 'status_response')
    readonly_fields = ('id', 'ip', 'date_log', 'http_method', 'url', 'status_response', 'size_response', 'user_agent')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Log, LogAdmin)

