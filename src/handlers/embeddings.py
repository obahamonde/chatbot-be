import asyncio
from os import name

from ..schemas.openai import OpenAIClient, OpenAIEmbeddingRequest
from ..schemas.pinecone import (PineConeClient, PineconeVector,
                                PineconeVectorQuery, PineconeVectorUpsert)


class OPStack:
    @property
    def openai(self):
        return OpenAIClient()
    
    @property
    def pinecone(self):
        return PineConeClient()
    
    async def ingest_embedding(self, namespace:str, text:str):
        embedding = await self.openai.post_embeddings(OpenAIEmbeddingRequest(input=text))
        vector = embedding.data[0].embedding
        await self.pinecone.upsert(PineconeVectorUpsert(namespace=namespace, vectors=[PineconeVector(values=vector, metadata={"text": text})]))
    
    async def query_embedding(self, namespace:str, text:str):
        embedding = await self.openai.post_embeddings(OpenAIEmbeddingRequest(input=text))
        vector = embedding.data[0].embedding
        response = await self.pinecone.query(PineconeVectorQuery(namespace=namespace, vector=vector))
        return response
    
    async def batch_ingest(self, namespace:str, texts:list[str]):
        await asyncio.gather(*[self.ingest_embedding(namespace, text) for text in texts])