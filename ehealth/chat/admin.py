from django.contrib import admin
from chat.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender','to','body',"timestamp")

admin.site.register(Message, MessageAdmin)