import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """
       This WebSocket consumer handles real-time notifications for clients.
       allowing clients to join a group, receive notified when have message.

       Methods:
       - connect: When a client connects, they join the "test" group.
       - receive: When a message is received, it's broadcast to the group.
       - send_notification: Sends a notification message to the client.
       - disconnect: When a client disconnects, they leave the group then delete the client from cache.
    """

    async def connect(self):
        self.channel_group_name = "test"
        self.room_group_name = "test"
        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def send_notification(self, data):
        await self.send_json(
            {"test": f"{data}"}
        )

    async def disconnect(self, code):
        channel_group_name = "test"
        await self.channel_layer.group_discard(
            channel_group_name,
            self.channel_name
        )
        await self.close()

