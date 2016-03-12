from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['content']}),
        ('Date information', {'fields': ['published'], 'classes':
                              ['collapse']}),
        # prob can delete userinfo just playing around
        ('User information', {'fields': ['author']})
    ]
    list_display = ('content', 'published', 'author')
    list_filter = ['published']
admin.site.register(Post, PostAdmin)
