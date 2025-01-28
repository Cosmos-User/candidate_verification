# load data from the storage and uploads embeedings to the vector db
from faceai import FaceAI
from db_connections.qdrant import QdrantConnection 


face = FaceAI()


class UploadEmbeddings:
    def __init__(self) -> None:
        pass

    async def upload_embeddings(self):
        embeddings , file_path = await face.get_face_embeddings()
        

