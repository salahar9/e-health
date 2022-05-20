from django.db import models

from landing.models import Person
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

	 

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
            'type': 'recieve.msg',
            'message': f"{to}"
        }
        notification_to = {
            'type': 'recieve.msg',
            'message': f"{sender}"
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(sender.pk, notification_sender)
        async_to_sync(channel_layer.group_send)(to.pk, notification_to)
    def save(self, *args, **kwargs):
        self.body = self.body.strip() 
        super(MessageModel, self).save(*args, **kwargs)
        self.notify_ws_clients()
    class Meta:
        ordering = ('-timestamp',)