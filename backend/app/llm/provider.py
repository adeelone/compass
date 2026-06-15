from typing import Protocol


class LLMProvider(Protocol):
    async def complete_json(self, prompt: str, schema_name: str) -> dict:
        ...


class MockLLMProvider:
    async def complete_json(self, prompt: str, schema_name: str) -> dict:
        return {"schema": schema_name, "rationale": "Mock provider used; no external model call was made."}

