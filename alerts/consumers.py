import json
from channels.generic.websocket import WebsocketConsumer

class AlertsConsumer(WebsocketConsumer):
    def connect(self):        
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = 'hello word'

        self.send(text_data=json.dumps({
            'message': message
        }))
