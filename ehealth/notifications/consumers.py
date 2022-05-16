
import json
import logging
from channels.generic.websocket import WebsocketConsumer

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

        self.send(text_data=json.dumps({

            'message': visite["infos"],
            "name":visite["name"],
            "img":visite["img"],
            "email":visite["email"],
            "sexe":visite["sexe"],
            "username":visite["username"],
            "adress":visite["adress"],
            "ville":visite["ville"],
            "phone":visite["phone"],
            
        }
        )
        )

    

