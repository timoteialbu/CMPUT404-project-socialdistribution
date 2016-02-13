from django.contrib import admin
##from django.contrib.auth.models import User

from .models import Post

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['post_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':
                              ['collapse']}),
        ('User information', {'fields': ['author']}) ##prob can delete userinfo just playing around
    ]
    list_display = ('post_text', 'pub_date', 'author')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Post, PostAdmin)


