import json, channels
from  asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from data_cabina.models import Company
from django.contrib.auth.models import User
from .models import *

class AlertsConsumer(AsyncWebsocketConsumer):
    """
        This consumer allows sending alerts to all users of a company.
    """
    async def connect(self):
        self.user = self.scope['user']
        #Check if user is authenticated
        if self.user.is_authenticated:
            #Check if user is bounded to a company
            try:
                self.company = await self.get_company()
            except:
                return
            #Join company group
            await self.channel_layer.group_add(str(self.company.id),self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave company group
        try:
            await self.channel_layer.group_discard(str(self.company.id),self.channel_name)
        except:
            pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Send message to company group
        await self.channel_layer.group_send(
            str(self.company.id),
            {
                'type': 'cabin_alert',
                'alert': 'ALERT!'
            }
        )

    async def cabin_alert(self, event):
        #Dict to json text
        text_data = json.dumps(event)
        #Send data to clients
        await self.send(text_data= text_data)
        #Save alert into database.
        await self.save_alert(text_data)

    @database_sync_to_async
    def get_company(self):
        user = User.objects.get(id=self.scope['user'].id)
        return user.client.company

    @database_sync_to_async
    def save_alert(self, message):
        Alert.objects.create(user = self.user, message = message)
