from dataclasses import dataclass
from datetime import datetime
from typing import *
from uuid import UUID, uuid4

from aiofauna import ApiClient  # pylint: disable=import-error
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

Vector = List[float]
Scalar = Union[float, int, str, bool]
Metadata = Dict[str, Scalar]
Context = List[Metadata]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

T = TypeVar("T", bound=BaseModel)


@dataclass
class Client(ApiClient):
    base_url: str
    headers: Dict[str, str]

    def __post_init__(self):
        super().__init__(base_url=self.base_url, headers=self.headers)

    async def fetch(
        self,
        endpoint: str,
        method: Method,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        if headers is None:
            headers = self.headers
        return await super().fetch(
            url=self.base_url + endpoint, method=method, headers=headers, json=json
        )

    async def stream(
        self,
        endpoint: str,
        method: Method,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        if headers is None:
            headers = self.headers
        async for chunk in super().stream(
            url=self.base_url + endpoint, method=method, headers=headers, json=json
        ):
            yield chunk

    async def text(
        self,
        endpoint: str,
        method: Method,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        if headers is None:
            headers = self.headers
        return await super().text(
            url=self.base_url + endpoint, method=method, headers=headers, json=json
        )

    async def blob(
        self,
        endpoint: str,
        method: Method,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        if headers is None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(
                method=method,
                url=self.base_url + endpoint,
                headers=headers,
                json=json,
            ) as response:
                return await response.read()

    async def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        return await self.fetch(endpoint=endpoint, method="GET", headers=headers)

    async def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        return await self.fetch(
            endpoint=endpoint, method="POST", headers=headers, json=json
        )

    async def put(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        return await self.fetch(
            endpoint=endpoint, method="PUT", headers=headers, json=json
        )

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        return await self.fetch(
            endpoint=endpoint, method="DELETE", headers=headers, json=json
        )

    async def patch(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ):
        return await self.fetch(
            endpoint=endpoint, method="PATCH", headers=headers, json=json
        )
