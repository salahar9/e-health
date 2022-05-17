from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)
from landing import Person
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

	

class MessageModel(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    sender= ForeignKey(Person, on_delete=CASCADE, verbose_name='user',)
	to= ForeignKey(Person, on_delete=CASCADE, verbose_name='recipient')
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False)
    body = TextField('body')

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """

        notification = {
            'type': 'recieve.msg',
            'message': '{}'.format(self.id)
        }
        channel_layer = get_channel_layer()
        #async_to_sync(channel_layer.group_send)(sender.pk, notification)
        async_to_sync(channel_layer.group_send)(to.pk, notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)