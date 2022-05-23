from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
import logging
logger=logging.getLogger(__name__)
from chat.models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        logger.warning("HEEEEEERE")
        async_to_sync(self.channel_layer.group_add)( 
            self.scope["user"].person.pk,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)( 
            self.scope["user"].person.pk,
            self.channel_name
        )
       
    def receive(self, text_data=None,bytes_data = None):
        logger.error(text_data)
        #text_data_json = json.loads(text_data)
        message = text_data
        # Send message to room group
        self.channel_layer.group_send(
             self.scope["user"].person.pk,
            {
                'type': 'recieve_message',
                'message': message
            }
        )

    def receive_msg(self,message):
        logger.error(message)
        self.send(text_data=json.dumps(
            {

            'message': "message",
           
            
            }
        )
