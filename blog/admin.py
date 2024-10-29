from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'image',)
    list_filter = ('title','id',)
    search_fields = ('id','title',)
