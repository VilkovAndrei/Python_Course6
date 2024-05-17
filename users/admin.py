from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'comment')
    # list_filter = ['country']
    search_fields = ('email', 'phone')
