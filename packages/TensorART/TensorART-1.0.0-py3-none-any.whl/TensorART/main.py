import aiohttp

class TensorClient():
    def __init__(self):
        self.url = 'https://tensorapi.onrender.com'
    async def create(self,model_id,prompt):
        url = f"{self.url}/generate/"
        try:
            data = None
            async with aiohttp.ClientSession() as session:
                async with session.post(url,json={'model':model_id,'prompt':prompt}) as response:
                    data = await response.json()
            return {'url': data}
        except Exception as e:
            return e
        