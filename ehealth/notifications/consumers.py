
import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from doctor.models import Visite
import channels.layers


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
        text_data_json = json.loads(visite)
        message = text_data_json['infos']
        self.send(text_data=json.dumps(
            {

            'message': message,
           
            
            }
        )
        )

  
class VisitePharmaConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)( self.scope["user"].person.pharmacie.INP, self.channel_name)
        self.accept()

    def disconnect(self,y):
        async_to_sync(self.channel_layer.group_discard)(
            self.scope["user"].person.pharmacie.INP, self.channel_name
            )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({

            'message': self.scope['user'].person.nom
        }))
    def send_visite(self,visite):
        text_data_json = json.loads(visite)
        message = text_data_json['infos']
        self.send(text_data=json.dumps(
            {

            'message': message,
           
            
            }
        )
        )


