from django.contrib import admin
from django.contrib.auth import get_permission_codename

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
    actions = ['make_published']

    def make_published(self, request, queryset):
        for post in queryset:
            post.publish()
    make_published.allowed_permissions = ['publish']
    make_published.short_description = "Publish Post"

    def has_publish_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('publish', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

admin.site.register(Post, PostAdmin)

admin.site.register(Tag)
