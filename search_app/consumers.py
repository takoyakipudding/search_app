from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Product  # Product model をインポート

class SearchConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        query = content.get('query', '')
        products = await Product.objects.filter(name__icontains=query).aget()  # ORM操作を非同期にするためにawaitを使用
        await self.send_json({
            'results': [{'name': product.name, 'price': product.price} for product in products]
        })
