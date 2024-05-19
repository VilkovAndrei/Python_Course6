from django.contrib import admin

from main.models import Client, MessageMailing, Mailing, AttemptMailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment', 'owner')
    list_filter = ['owner']
    search_fields = ('email', 'name')


@admin.register(MessageMailing)
class MessageMailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'owner')
    list_filter = ('subject', 'owner')
    search_fields = ('body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'frequency_mailing', 'status_mailing', 'message', 'owner')
    list_filter = ('start_time', 'owner')
    search_fields = ('status_mailing', 'frequency_mailing')


@admin.register(AttemptMailing)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_last_mailing', 'server_response', 'mailing')
    list_filter = ('time_last_mailing',)
    search_fields = ('server_response', 'mailing')
