from dataclasses import dataclass
from time import monotonic


@dataclass
class TokenBucket:
    rate_per_second: float
    burst: int
    tokens: float = 0
    updated_at: float = 0

    def __post_init__(self) -> None:
        self.tokens = float(self.burst)
        self.updated_at = monotonic()

    def allow(self, cost: int = 1) -> bool:
        now = monotonic()
        elapsed = now - self.updated_at
        self.updated_at = now
        self.tokens = min(float(self.burst), self.tokens + elapsed * self.rate_per_second)
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True

