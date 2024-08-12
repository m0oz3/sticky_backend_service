import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django_celery_beat.models import PeriodicTask


class GameConsumer(AsyncWebsocketConsumer):
    state = {"player1": {}, "player2": {}}

    async def connect(self):
        await self.channel_layer.group_add("game_room", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game_room", self.channel_name)
        things = await database_sync_to_async(PeriodicTask.objects.filter)(
            name="Ticker for game",
            task="game_tick",
        )
        await database_sync_to_async(things.delete())()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "state":
            text_data_json = text_data_json["data"]
            self.state.update(text_data_json)
            await self.channel_layer.group_send(
                "game_room",
                {"type": "state_update", "data": self.state},
            )

    async def state_update(self, text_data):
        await self.send(json.dumps({"type": "state", "data": text_data["data"]}))
