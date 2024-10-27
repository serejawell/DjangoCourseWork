from django.contrib import admin

from newsletter.models import Message, Newsletter


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message',)

@admin.register(Newsletter)
class Newsletter(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('created_at', 'scheduled_at', 'status',)
