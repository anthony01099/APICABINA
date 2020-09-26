import json, channels
from  asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from data_cabina.models import Company
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Cabin

class BoothConsumer(AsyncWebsocketConsumer):
    """
        This consumer allows sending alerts to all users of a company.
    """
    async def connect(self):
        self.booth_token = self.scope['url_route']['kwargs']['booth_token']
        try:
            booth = await self.get_booth()
        except:
            return
        else:
            #Join company group
            await self.channel_layer.group_add(self.booth_token,self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave company group
        try:
            await self.channel_layer.group_discard(self.booth_token,self.channel_name)
        except:
            pass

    async def booth_info(self, event):
        #Dict to json text
        text_data = json.dumps(event)
        #Send data to clients
        await self.send(text_data= text_data)

    @database_sync_to_async
    def get_booth(self):
        return Cabin.objects.get(token__id=self.booth_token)
