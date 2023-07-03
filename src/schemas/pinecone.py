from ..config import *
from .models import *
from .typedefs import *


class PineConeSparsedValues(BaseModel):
    """
    A class used to represent the sparsed values of a Pinecone vector.

    Attributes
    ----------
    indices : List[int]
        The indices of the embedding.
    values : Vector
        The values of the embedding.
    """

    indices: List[int] = Field(..., description="The indices of the embedding.")
    values: Vector = Field(..., description="The values of the embedding.")


class PineconeVector(BaseModel):
    """
    A class used to represent a Pinecone vector.

    Attributes
    ----------
    id : str
        The ID of the embedding.
    values : Vector
        The values of the embedding.
    sparseValues : Optional[PineConeSparsedValues]
        The sparse values of the embedding.
    metadata : Metadata
        The metadata of the embedding. Must be a dictionary of strings.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="The ID of the embedding."
    )
    values: Vector = Field(..., description="The values of the embedding.")
    sparseValues: Optional[PineConeSparsedValues] = Field(
        default_factory=list, description="The sparse values of the embedding."
    )
    metadata: Metadata = Field(
        default_factory=dict,
        description="The metadata of the embedding. Must be a dictionary of strings.",
    )


class PineconeVectorUpsert(BaseModel):
    """
    A class used to represent an upsert operation on a Pinecone vector.

    Attributes
    ----------
    namespace : str
        The namespace of the embedding.
    vectors : List[PineconeVector]
        The vectors of the embedding.
    """

    namespace: str = Field(..., description="The namespace of the embedding.")
    vectors: List[PineconeVector] = Field(
        ..., description="The vectors of the embedding."
    )


class PineconeVectorQuery(BaseModel):
    """
    A class used to represent a query on a Pinecone vector.

    Attributes
    ----------
    namespace : str
        The namespace of the embedding.
    topK : int
        The number of results to return.
    vector : Vector
        The vector of the embedding.
    """

    namespace: str = Field(..., description="The namespace of the embedding.")
    topK: int = Field(default=8, description="The number of results to return.")
    vector: Vector = Field(..., description="The vector of the embedding")


class PineconeVectorMatch(BaseModel):
    """
    A class used to represent a match of a Pinecone vector.

    Attributes
    ----------
    id : str
        The ID of the embedding.
    score : float
        The score of the embedding.
    values : Vector
        The vector of the embedding.
    sparseValues : Optional[PineConeSparsedValues]
        The sparse values of the embedding.
    metadata : Optional[Metadata]
        The metadata of the embedding.
    """

    id: str = Field(..., description="The ID of the embedding.")
    score: float = Field(..., description="The score of the embedding.")
    values: Optional[Vector] = Field(None, description="The vector of the embedding.")
    sparseValues: Optional[PineConeSparsedValues] = Field(
        None, description="The sparse values of the embedding."
    )
    metadata: Optional[Metadata] = Field(
        None, description="The metadata of the embedding."
    )


class PineconeVectorResponse(BaseModel):
    """
    A class used to represent a response from a Pinecone vector request.

    Attributes
    ----------
    matches : List[PineconeVectorMatch]
        The matches of the embedding.
    namespace : str
        The namespace of the embedding.
    """

    matches: List[PineconeVectorMatch] = Field(
        ..., description="The matches of the embedding."
    )
    namespace: str = Field(..., description="The namespace of the embedding.")


class PineConeClient(Client):
    """
    A class used to represent a Pinecone client.
    """

    base_url = env.PINECONE_API_URL
    headers = {
        "Content-Type": "application/json",
        "api-key": env.PINECONE_API_KEY,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def upsert(self, request: PineconeVectorUpsert):
        await self.post("/vectors/upsert", json=request.dict())

    async def query(self, request: PineconeVectorQuery):
        response = await self.post("/query", json=request.dict())
        assert isinstance(response, dict)
        return PineconeVectorResponse(**response)
