import os
from qdrant_client import AsyncQdrantClient, models
import asyncio
from dotenv import load_dotenv


load_dotenv()

class QdrantConnection:
    
    def __init__(self) -> None:
        self.url = os.getenv('QDRANT_URL')
        self.port = os.getenv('QDRANT_PORT')
        self.client = AsyncQdrantClient(url=self.url, port=self.port, timeout=60)

    async def create_collection(self, collection_name):
       try:
        result = await self.client.create_collection(
                collection_name=f"{collection_name}",
                vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE))
        
        return result
       
       except Exception as e:
          print(e)

    async def check_collection_existance(self, collection_name):
        try:
            result = await self.client.collection_exists(collection_name=f"{collection_name}")
            return result
        except Exception as e:
            print(e)

    async def deletect_collection(self, collection_name):

        try:
            result = self.client.delete_collection(collection_name=f"{collection_name}")
            return result

        except Exception as e:
            print(e)
    
    async def get_collection_info(self,collection_name):
            try:
                result = await self.client.get_collection()
                return result
             
            except Exception as e:
                print(e)

    async def list_all_collection(self):
        try:
            result = await self.client.get_collections()
            return result 
        
        except Exception as e:
            print(e)

qdrant_client = QdrantConnection()

if __name__ == "__main__":
    result = asyncio.run(qdrant_client.list_all_collection())
    print(result)