from channels.generic.websocket import AsyncJsonWebsocketConsumer
from ..models import WebsocketClient

class TrackingBgTask(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress_id = None
    
    async def connect(self):
        self.progress_id = self.scope.get('url_route')['kwargs'].get('progress_id')

        client, created = await WebsocketClient.objects.aupdate_or_create(
            progress_id=self.progress_id,
            defaults={'channel_name': self.channel_name}

        )
        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnect called')
        await WebsocketClient.objects.filter(progress_id=self.progress_id).aupdate(channel_name=None)

        
    async def receive_json(self, content, **kwargs):
        print(content)
    
    async def new_message(self, event):
        await self.send_json({'new_message': event})
