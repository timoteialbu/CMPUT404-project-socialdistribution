from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['post_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':
                              ['collapse']}),
        # prob can delete userinfo just playing around
        ('User information', {'fields': ['author']})
    ]
    list_display = ('post_text', 'pub_date', 'author')
    list_filter = ['pub_date']
admin.site.register(Post, PostAdmin)
