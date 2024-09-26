from django.contrib import admin

from newsletter.models import User, Message, Newsletter


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'email',)
    list_editable = ('first_name', 'last_name', 'middle_name', 'email',)
    list_filter = ('email',)
    search_fields = ('email', 'first_name', 'last_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message',)


@admin.register(Newsletter)
class Newsletter(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('created_at', 'scheduled_at', 'status',)
