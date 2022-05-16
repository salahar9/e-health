
import json
import logging
from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from doctor.models import Visite
import channels.layers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers import serialize

class VisiteConsumer(WebsocketConsumer):
    def connect(self):
        
        async_to_sync(self.channel_layer.group_add)( self.scope["user"].person.doctor.INP, self.channel_name)
        self.accept()

    def disconnect(self,y):
                async_to_sync(self.channel_layer.group_discard)(self.scope["user"].person.doctor.INP, self.channel_name)


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({

            'message': self.scope['user'].person.nom
        }))
    def send_visite(self,visite):

        self.send(text_data=json.dumps({

            'message': visite["visite"]
            
        }))
        logging.info("sent to clientt")

    @receiver(post_save, sender=Visite)
        
    def up(sender, instance,**kwargs):
        logging.info("signal")
        channel_layer=get_channel_layer()
        group=instance.medcin_id.INP
        async_to_sync(channel_layer.group_send)(group, {
            'type': 'send.visite',
            "visite":instance.pk,
            "name":instance.patient_id.person_id.nom+" "+instance.patient_id.person_id.prenom,
            "img":instance.patient_id.person_id.img.url,
            "email":instance.patient_id.person_id.user.email,
            "sexe":instance.patient_id.person_id.sexe,
            "username":instance.patient_id.person_id.user.username,
            "adress":instance.patient_id.person_id.adress,
            "ville":instance.patient_id.person_id.ville,
            "phone":instance.patient_id.person_id.phone,

            }
    )

