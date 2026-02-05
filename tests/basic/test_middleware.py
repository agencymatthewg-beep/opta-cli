"""
Tests for production middleware.
"""

import time
import pytest
from unittest.mock import Mock, patch

from opta.middleware import (
    ProductionMiddleware,
    MiddlewareConfig,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    RateLimiter,
    RateLimiterConfig,
    RetryHandler,
    RetryConfig,
    CircuitOpenError,
    RateLimitExceededError,
    get_middleware,
    configure_middleware,
    reset_middleware,
)


class TestCircuitBreaker:
    def test_initial_state_closed(self):
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_opens_after_threshold_failures(self):
        config = CircuitBreakerConfig(failure_threshold=3)
        cb = CircuitBreaker(config)

        for _ in range(3):
            cb.record_failure()

        assert cb.state == CircuitState.OPEN

    def test_can_execute_when_closed(self):
        cb = CircuitBreaker()
        assert cb.can_execute() is True

    def test_cannot_execute_when_open(self):
        config = CircuitBreakerConfig(failure_threshold=1)
        cb = CircuitBreaker(config)
        cb.record_failure()

        assert cb.state == CircuitState.OPEN
        assert cb.can_execute() is False

    def test_transitions_to_half_open(self):
        config = CircuitBreakerConfig(failure_threshold=1, recovery_timeout=0.1)
        cb = CircuitBreaker(config)
        cb.record_failure()

        assert cb.state == CircuitState.OPEN
        time.sleep(0.15)
        assert cb.state == CircuitState.HALF_OPEN

    def test_closes_after_success_in_half_open(self):
        config = CircuitBreakerConfig(
            failure_threshold=1,
            recovery_timeout=0.1,
            success_threshold=2,
        )
        cb = CircuitBreaker(config)
        cb.record_failure()

        time.sleep(0.15)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        cb.record_success()
        assert cb.state == CircuitState.CLOSED

    def test_reset(self):
        config = CircuitBreakerConfig(failure_threshold=1)
        cb = CircuitBreaker(config)
        cb.record_failure()

        assert cb.state == CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED


class TestRateLimiter:
    def test_allows_within_limit(self):
        config = RateLimiterConfig(requests_per_minute=10)
        rl = RateLimiter(config)

        can_proceed, wait_time = rl.can_proceed()
        assert can_proceed is True
        assert wait_time is None

    def test_blocks_when_limit_exceeded(self):
        config = RateLimiterConfig(requests_per_minute=2, burst_allowance=1.0)
        rl = RateLimiter(config)

        # Record requests to exceed limit
        rl.record_request()
        rl.record_request()

        can_proceed, wait_time = rl.can_proceed()
        assert can_proceed is False
        assert wait_time is not None

    def test_respects_token_limit(self):
        config = RateLimiterConfig(tokens_per_minute=100, burst_allowance=1.0)
        rl = RateLimiter(config)

        rl.record_request(tokens_used=100)

        can_proceed, wait_time = rl.can_proceed(estimated_tokens=10)
        assert can_proceed is False


class TestRetryHandler:
    def test_calculates_delay_with_backoff(self):
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=0)
        rh = RetryHandler(config)

        # Attempt 0: 1 * 2^0 = 1
        delay0 = rh.calculate_delay(0)
        assert 0.9 <= delay0 <= 1.1

        # Attempt 1: 1 * 2^1 = 2
        delay1 = rh.calculate_delay(1)
        assert 1.8 <= delay1 <= 2.2

        # Attempt 2: 1 * 2^2 = 4
        delay2 = rh.calculate_delay(2)
        assert 3.6 <= delay2 <= 4.4

    def test_respects_max_delay(self):
        config = RetryConfig(base_delay=10.0, max_delay=5.0, jitter=0)
        rh = RetryHandler(config)

        delay = rh.calculate_delay(10)
        assert delay <= 5.0

    def test_should_retry_respects_max_retries(self):
        config = RetryConfig(max_retries=2)
        rh = RetryHandler(config)

        # Mock an exception that should be retried
        with patch("opta.exceptions.LiteLLMExceptions") as mock_ex_class:
            mock_ex = Mock()
            mock_ex.get_ex_info.return_value = Mock(retry=True)
            mock_ex_class.return_value = mock_ex

            assert rh.should_retry(0, Exception()) is True
            assert rh.should_retry(1, Exception()) is True
            assert rh.should_retry(2, Exception()) is False  # Max reached


class TestProductionMiddleware:
    def test_executes_successfully(self):
        middleware = ProductionMiddleware()
        result = middleware.execute(lambda: "success")

        assert result == "success"
        assert middleware.metrics.successful_requests == 1
        assert middleware.metrics.failed_requests == 0

    def test_raises_circuit_open_error(self):
        config = MiddlewareConfig(
            circuit_breaker=CircuitBreakerConfig(failure_threshold=1)
        )
        middleware = ProductionMiddleware(config)

        # Force circuit to open
        middleware.circuit_breaker.record_failure()

        with pytest.raises(CircuitOpenError):
            middleware.execute(lambda: "test")

        assert middleware.metrics.circuit_breaker_rejections == 1

    def test_raises_rate_limit_error(self):
        config = MiddlewareConfig(
            rate_limiter=RateLimiterConfig(requests_per_minute=1, burst_allowance=1.0)
        )
        middleware = ProductionMiddleware(config)

        # Use up the rate limit
        middleware.rate_limiter.record_request()

        with pytest.raises(RateLimitExceededError):
            middleware.execute(lambda: "test")

        assert middleware.metrics.rate_limit_rejections == 1

    def test_disabled_middleware_passes_through(self):
        config = MiddlewareConfig(enabled=False)
        middleware = ProductionMiddleware(config)

        # Even with circuit open, disabled middleware should pass through
        middleware.circuit_breaker.record_failure()
        middleware.circuit_breaker.record_failure()
        middleware.circuit_breaker.record_failure()
        middleware.circuit_breaker.record_failure()
        middleware.circuit_breaker.record_failure()

        result = middleware.execute(lambda: "success")
        assert result == "success"

    def test_metrics_tracking(self):
        middleware = ProductionMiddleware()

        middleware.execute(lambda: "test")
        middleware.record_cost(0.01)
        middleware.record_tokens_sent(100)

        metrics = middleware.get_metrics()
        assert metrics["total_requests"] == 1
        assert metrics["successful_requests"] == 1
        assert metrics["total_cost"] == 0.01
        assert metrics["total_tokens_sent"] == 100


class TestGlobalMiddleware:
    def test_get_middleware_returns_singleton(self):
        reset_middleware()
        m1 = get_middleware()
        m2 = get_middleware()
        assert m1 is m2

    def test_configure_middleware_replaces_instance(self):
        reset_middleware()
        m1 = get_middleware()

        config = MiddlewareConfig(enabled=False)
        configure_middleware(config)

        m2 = get_middleware()
        assert m1 is not m2
        assert m2.config.enabled is False
