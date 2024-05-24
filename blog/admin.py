from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'preview', 'created_at', 'is_published', 'count_view', 'author',)
    list_filter = ('is_published', 'author',)
    search_fields = ('title',)
