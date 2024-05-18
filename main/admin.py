from django.contrib import admin

from main.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment', 'owner')
    list_filter = ['owner']
    search_fields = ('email', 'name')
