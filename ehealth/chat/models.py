from django.db import models

from landing.models import Person
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

	 
import logging
class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE,related_name="message_sender")
    to = models.ForeignKey(Person, on_delete=models.CASCADE,related_name="message_to")
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False)
    body = models.TextField('body')
    seen=models.BooleanField(default=False)
    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """

        notification_sender = {
            'type': 'chat.receive.msg',
            'message': f"{self.to}"
        }
        notification_to = {
            'type': 'receive.msg',
            'message': f"{self.sender}"
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(self.sender.pk, notification_sender)
        async_to_sync(channel_layer.group_send)(self.to.pk, notification_to)
    def save(self, *args, **kwargs):
       
        self.body = self.body.strip() 
        super(Message, self).save(*args, **kwargs)
        self.notify_ws_clients()
    class Meta:
        ordering = ('-timestamp',)