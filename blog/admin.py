from django.contrib import admin
from .models import Post, Tag, Comment, AuthorProfile



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
