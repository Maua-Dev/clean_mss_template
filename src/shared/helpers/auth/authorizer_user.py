"""Helpers for API Gateway authorizer → Lambda request.

Contrato do context: apenas claims Microsoft — sub, mail, name.
Role / User de domínio NÃO entram aqui; isso é responsabilidade do usecase.
"""
from __future__ import annotations

import json
from typing import Any, Optional

# chave única em request.data — controllers usam request.data.get(USER_FROM_AUTHORIZER_KEY)
USER_FROM_AUTHORIZER_KEY = "user_from_authorizer"


def build_authorizer_user_context(*, sub: str, mail: str, name: str) -> dict[str, str]:
    """
    Monta o context do TOKEN authorizer só com claims Microsoft.

    Args:
        sub: identificador do usuário no IdP (Graph `id` / JWT `sub`)
        mail: e-mail
        name: nome de exibição
    """
    return {
        "user": json.dumps(
            {
                "sub": sub,
                "mail": mail,
                "name": name,
            }
        )
    }


def parse_authorizer_user_from_event(event: dict | None) -> Optional[dict[str, Any]]:
    """
    Lê o usuário injetado pelo TOKEN authorizer.

    API Gateway REST coloca o context em:
      event["requestContext"]["authorizer"]["user"]  # string JSON

    Retorno esperado: {"sub", "mail", "name"} ou None.
    """
    if not event:
        return None

    authorizer = (event.get("requestContext") or {}).get("authorizer") or {}
    raw_user = authorizer.get("user")
    if raw_user is None:
        return None

    if isinstance(raw_user, dict):
        parsed = raw_user
    elif isinstance(raw_user, str):
        try:
            parsed = json.loads(raw_user)
        except (TypeError, json.JSONDecodeError):
            return None
        if not isinstance(parsed, dict):
            return None
    else:
        return None

    sub = parsed.get("sub")
    mail = parsed.get("mail")
    name = parsed.get("name")
    if not isinstance(sub, str) or not isinstance(mail, str) or not isinstance(name, str):
        return None
    if not sub.strip() or not mail.strip():
        return None

    return {"sub": sub, "mail": mail, "name": name}
