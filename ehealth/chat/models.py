from django.db import models

from landing.models import Person
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

	 

class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE,related_name="message")
    to = models.ForeignKey(Person, on_delete=models.CASCADE,related_name="message")
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False)
    body = models.TextField('body')
    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """

        notification = {
            'type': 'recieve.msg',
            'message': '{}'.format(self.id)
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(sender.pk, notification)
        async_to_sync(channel_layer.group_send)(to.pk, notification)
    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        self.notify_ws_clients()
    class Meta:
        ordering = ('-timestamp',)