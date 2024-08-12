from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


async def closing_send(channel_layer, channel, message):
    await channel_layer.send(channel, message)
    await channel_layer.close_pools()


async def closing_group_send(channel_layer, group_name, message):
    await channel_layer.group_send(group_name, message)
    await channel_layer.close_pools()


@shared_task(name="game_tick")
def game_tick():
    group_name = "game_room"
    async_to_sync(closing_group_send)(channel_layer, group_name, {"type": "tick"})
