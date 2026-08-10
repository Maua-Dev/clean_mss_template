"""
Observability invisível para quem escreve módulos.

Novos devs só precisam disto no presenter:

    from src.shared.helpers.observability.wrap_handler import observed_handler

    @observed_handler("create_user")
    def lambda_handler(event, context):
        ...

Controller / usecase / viewmodel não recebem observability.
Powertools (quando STAGE != TEST) fica encapsulado em ObservabilityAWS.
"""
from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from src.shared.environments import Environments

F = TypeVar("F", bound=Callable[..., Any])


def observed_handler(module_name: str) -> Callable[[F], F]:
    """Aplica logging / metrics / tracing sem poluir o código de negócio."""

    def decorator(handler: F) -> F:
        observability = Environments.get_observability()(module_name=module_name)

        @wraps(handler)
        def inner(event: Any, context: Any) -> Any:
            start = time.monotonic()
            response = handler(event, context)
            elapsed_ms = (time.monotonic() - start) * 1000
            observability.add_metric(
                name="ProcessingTime", unit="Milliseconds", value=elapsed_ms
            )
            if (
                isinstance(response, dict)
                and response.get("statusCode") is not None
                and response["statusCode"] >= 400
            ):
                observability.add_metric(name="ErrorCount", unit="Count", value=1)
            return response

        return observability.handler_decorators(inner)

    return decorator
