import os 
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

class RedisConnection:
    def __init__(self) -> None:
        self.client = redis.Redis(host=os.getenv('REDIS_URL'), port=os.getenv('REDIS_PORT'))
        
        pass

    
    
    