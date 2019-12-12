from django.contrib import admin

# Register your models here.
from django.contrib import admin
from blog.models import Post, Comment, Tag

class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date']
    filter_horizontal = ['tags']
    inlines = [CommentInlineAdmin]

admin.site.register(Post, PostAdmin)

admin.site.register(Tag)
