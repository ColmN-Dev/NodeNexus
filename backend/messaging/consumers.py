import json

from channels.generic.websocket import AsyncWebsocketConsumer

# WebSocket consumer for handling notifications.
# This consumer manages WebSocket connections for authenticated users, allowing them to receive real-time notifications.
class NotificationConsumer(AsyncWebsocketConsumer):

    # Connect to the WebSocket and add the user to a notification group if authenticated.
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            self.group_name = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    # Disconnect from the WebSocket and remove the user from the notification group.
    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive a notification event and send it to the WebSocket.
    async def notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'url': event['url'],
            'created_at': event['created_at'],
        }))