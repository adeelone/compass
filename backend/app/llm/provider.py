from typing import Any
from typing import Protocol


class LLMProvider(Protocol):
    async def complete_json(self, prompt: str, schema_name: str) -> dict[str, Any]:
        ...


class MockLLMProvider:
    async def complete_json(self, prompt: str, schema_name: str) -> dict[str, Any]:
        return {"schema": schema_name, "rationale": "Mock provider used; no external model call was made."}
