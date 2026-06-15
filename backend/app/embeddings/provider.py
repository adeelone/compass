from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed(self, text: str) -> list[float]:
        ...


class MockEmbeddingProvider:
    async def embed(self, text: str) -> list[float]:
        return [float((sum(text.encode("utf-8")) % 97) / 97)]

