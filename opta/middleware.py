"""
Production Middleware for Opta CLI

Provides reliability patterns for LLM API calls:
- Circuit Breaker: Prevents cascading failures
- Rate Limiter: Prevents quota exhaustion
- Enhanced Retry: Exponential backoff with jitter
- Metrics: Token/cost tracking and observability
"""

import random
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Optional

from opta.dump import dump  # noqa: F401


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""

    failure_threshold: int = 5  # Failures before opening
    recovery_timeout: float = 30.0  # Seconds before trying again
    half_open_max_calls: int = 3  # Test calls in half-open state
    success_threshold: int = 2  # Successes to close from half-open


@dataclass
class RateLimiterConfig:
    """Configuration for rate limiter."""

    requests_per_minute: int = 60
    tokens_per_minute: int = 100000
    burst_allowance: float = 1.5  # Allow 1.5x burst


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: float = 0.1  # 10% jitter


@dataclass
class MiddlewareMetrics:
    """Tracks middleware metrics."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    retried_requests: int = 0
    circuit_breaker_rejections: int = 0
    rate_limit_rejections: int = 0
    total_tokens_sent: int = 0
    total_tokens_received: int = 0
    total_cost: float = 0.0
    last_request_time: Optional[float] = None
    average_latency_ms: float = 0.0
    _latencies: deque = field(default_factory=lambda: deque(maxlen=100))

    def record_latency(self, latency_ms: float):
        self._latencies.append(latency_ms)
        if self._latencies:
            self.average_latency_ms = sum(self._latencies) / len(self._latencies)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "retried_requests": self.retried_requests,
            "circuit_breaker_rejections": self.circuit_breaker_rejections,
            "rate_limit_rejections": self.rate_limit_rejections,
            "total_tokens_sent": self.total_tokens_sent,
            "total_tokens_received": self.total_tokens_received,
            "total_cost": self.total_cost,
            "average_latency_ms": self.average_latency_ms,
            "success_rate": (
                self.successful_requests / self.total_requests
                if self.total_requests > 0
                else 0.0
            ),
        }


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests are rejected immediately
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(self, config: Optional[CircuitBreakerConfig] = None):
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._half_open_calls = 0
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                if (
                    self._last_failure_time
                    and time.time() - self._last_failure_time >= self.config.recovery_timeout
                ):
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
                    self._success_count = 0
            return self._state

    def can_execute(self) -> bool:
        state = self.state
        if state == CircuitState.CLOSED:
            return True
        if state == CircuitState.OPEN:
            return False
        # HALF_OPEN: allow limited calls
        with self._lock:
            if self._half_open_calls < self.config.half_open_max_calls:
                self._half_open_calls += 1
                return True
            return False

    def record_success(self):
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.config.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
            elif self._state == CircuitState.CLOSED:
                self._failure_count = max(0, self._failure_count - 1)

    def record_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
            elif (
                self._state == CircuitState.CLOSED
                and self._failure_count >= self.config.failure_threshold
            ):
                self._state = CircuitState.OPEN

    def reset(self):
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
            self._half_open_calls = 0


class RateLimiter:
    """
    Token bucket rate limiter.

    Tracks both request rate and token rate to prevent quota exhaustion.
    """

    def __init__(self, config: Optional[RateLimiterConfig] = None):
        self.config = config or RateLimiterConfig()
        self._request_timestamps: deque = deque()
        self._token_usage: deque = deque()  # (timestamp, tokens)
        self._lock = threading.Lock()

    def can_proceed(self, estimated_tokens: int = 0) -> tuple[bool, Optional[float]]:
        """
        Check if request can proceed.

        Returns:
            (can_proceed, wait_time_seconds)
        """
        now = time.time()
        window_start = now - 60.0  # 1 minute window

        with self._lock:
            # Clean old entries
            while self._request_timestamps and self._request_timestamps[0] < window_start:
                self._request_timestamps.popleft()
            while self._token_usage and self._token_usage[0][0] < window_start:
                self._token_usage.popleft()

            # Check request rate
            max_requests = int(self.config.requests_per_minute * self.config.burst_allowance)
            if len(self._request_timestamps) >= max_requests:
                wait_time = self._request_timestamps[0] - window_start
                return False, max(0.1, wait_time)

            # Check token rate
            total_tokens = sum(t[1] for t in self._token_usage)
            max_tokens = int(self.config.tokens_per_minute * self.config.burst_allowance)
            if total_tokens + estimated_tokens > max_tokens:
                if self._token_usage:
                    wait_time = self._token_usage[0][0] - window_start
                    return False, max(0.1, wait_time)

            return True, None

    def record_request(self, tokens_used: int = 0):
        now = time.time()
        with self._lock:
            self._request_timestamps.append(now)
            if tokens_used > 0:
                self._token_usage.append((now, tokens_used))


class RetryHandler:
    """
    Enhanced retry handler with exponential backoff and jitter.
    """

    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt with jitter."""
        delay = self.config.base_delay * (self.config.exponential_base**attempt)
        delay = min(delay, self.config.max_delay)

        # Add jitter
        jitter_range = delay * self.config.jitter
        delay += random.uniform(-jitter_range, jitter_range)

        return max(0.1, delay)

    def should_retry(self, attempt: int, exception: Exception) -> bool:
        """Determine if we should retry based on attempt count and exception type."""
        if attempt >= self.config.max_retries:
            return False

        # Import here to avoid circular imports
        from opta.exceptions import LiteLLMExceptions

        litellm_ex = LiteLLMExceptions()
        ex_info = litellm_ex.get_ex_info(exception)

        return ex_info.retry if ex_info.retry is not None else False


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""

    pass


class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, wait_time: float):
        self.wait_time = wait_time
        super().__init__(f"Rate limit exceeded. Retry after {wait_time:.1f}s")


@dataclass
class MiddlewareConfig:
    """Combined configuration for all middleware components."""

    circuit_breaker: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)
    rate_limiter: RateLimiterConfig = field(default_factory=RateLimiterConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    enabled: bool = True
    verbose: bool = False


class ProductionMiddleware:
    """
    Production middleware that wraps LLM API calls with reliability patterns.

    Usage:
        middleware = ProductionMiddleware()
        result = middleware.execute(litellm.completion, **kwargs)
    """

    def __init__(self, config: Optional[MiddlewareConfig] = None):
        self.config = config or MiddlewareConfig()
        self.circuit_breaker = CircuitBreaker(self.config.circuit_breaker)
        self.rate_limiter = RateLimiter(self.config.rate_limiter)
        self.retry_handler = RetryHandler(self.config.retry)
        self.metrics = MiddlewareMetrics()
        self._lock = threading.Lock()

    def execute(
        self,
        func: Callable,
        *args,
        estimated_tokens: int = 0,
        **kwargs,
    ) -> Any:
        """
        Execute a function with middleware protections.

        Args:
            func: The function to execute (e.g., litellm.completion)
            estimated_tokens: Estimated tokens for rate limiting
            *args, **kwargs: Arguments to pass to the function

        Returns:
            The result of the function

        Raises:
            CircuitOpenError: If circuit breaker is open
            RateLimitExceededError: If rate limit exceeded
        """
        if not self.config.enabled:
            return func(*args, **kwargs)

        with self._lock:
            self.metrics.total_requests += 1

        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            with self._lock:
                self.metrics.circuit_breaker_rejections += 1
            raise CircuitOpenError(
                f"Circuit breaker is {self.circuit_breaker.state.value}. "
                f"Service appears to be failing. Will retry in "
                f"{self.config.circuit_breaker.recovery_timeout}s."
            )

        # Check rate limiter
        can_proceed, wait_time = self.rate_limiter.can_proceed(estimated_tokens)
        if not can_proceed:
            with self._lock:
                self.metrics.rate_limit_rejections += 1
            raise RateLimitExceededError(wait_time)

        # Execute with retry
        last_exception = None
        for attempt in range(self.config.retry.max_retries + 1):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                latency_ms = (time.time() - start_time) * 1000

                # Record success
                self.circuit_breaker.record_success()
                with self._lock:
                    self.metrics.successful_requests += 1
                    self.metrics.record_latency(latency_ms)
                    self.metrics.last_request_time = time.time()

                # Record rate limit usage
                tokens_used = self._extract_tokens(result)
                self.rate_limiter.record_request(tokens_used)

                # Update token metrics
                if tokens_used > 0:
                    with self._lock:
                        self.metrics.total_tokens_received += tokens_used

                return result

            except Exception as e:
                last_exception = e

                if self.config.verbose:
                    print(f"[Middleware] Attempt {attempt + 1} failed: {type(e).__name__}: {e}")

                # Check if we should retry
                if not self.retry_handler.should_retry(attempt, e):
                    self.circuit_breaker.record_failure()
                    with self._lock:
                        self.metrics.failed_requests += 1
                    raise

                # Record retry
                with self._lock:
                    self.metrics.retried_requests += 1

                # Calculate and apply delay
                delay = self.retry_handler.calculate_delay(attempt)
                if self.config.verbose:
                    print(f"[Middleware] Retrying in {delay:.1f}s...")
                time.sleep(delay)

        # All retries exhausted
        self.circuit_breaker.record_failure()
        with self._lock:
            self.metrics.failed_requests += 1

        if last_exception:
            raise last_exception

    def _extract_tokens(self, result: Any) -> int:
        """Extract token count from API response."""
        try:
            if hasattr(result, "usage") and result.usage:
                return getattr(result.usage, "total_tokens", 0)
        except Exception:
            pass
        return 0

    def record_cost(self, cost: float):
        """Record cost from external calculation."""
        with self._lock:
            self.metrics.total_cost += cost

    def record_tokens_sent(self, tokens: int):
        """Record tokens sent."""
        with self._lock:
            self.metrics.total_tokens_sent += tokens

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        return self.metrics.to_dict()

    def get_status(self) -> Dict[str, Any]:
        """Get middleware status including circuit breaker state."""
        return {
            "enabled": self.config.enabled,
            "circuit_breaker_state": self.circuit_breaker.state.value,
            "metrics": self.get_metrics(),
        }

    def reset(self):
        """Reset middleware state."""
        self.circuit_breaker.reset()
        self.metrics = MiddlewareMetrics()


# Global middleware instance
_middleware: Optional[ProductionMiddleware] = None
_middleware_lock = threading.Lock()


def get_middleware() -> ProductionMiddleware:
    """Get or create the global middleware instance."""
    global _middleware
    with _middleware_lock:
        if _middleware is None:
            _middleware = ProductionMiddleware()
        return _middleware


def configure_middleware(config: MiddlewareConfig):
    """Configure the global middleware instance."""
    global _middleware
    with _middleware_lock:
        _middleware = ProductionMiddleware(config)


def reset_middleware():
    """Reset the global middleware instance."""
    global _middleware
    with _middleware_lock:
        if _middleware:
            _middleware.reset()
