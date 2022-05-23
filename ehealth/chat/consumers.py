from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
import logger
logger=logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        

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

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )

    def receive_msg(self,message):
        text_data_json = json.loads(message)
        message = text_data_json['message']
        # Send message to room group
        self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )
