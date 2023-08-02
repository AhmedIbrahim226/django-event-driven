from channels.layers import get_channel_layer
from ..models import WebsocketClient

async def progress_broadcast_message(progress_id, percentage, status):
    client = await WebsocketClient.objects.aget(progress_id=progress_id)
    channel_layer = get_channel_layer()

    await channel_layer.send(
        str(client.channel_name),
        {
            'type': 'new_message',
            'progress_id': progress_id,
            'percentage': percentage,
            'status': 'Finished' if percentage == 100 else status
        }
    )