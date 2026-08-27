#!/usr/bin/env python3
import os
import re

import aws_cdk as cdk

from adjust_layer_directory import adjust_layer_directory
from stack.iac_stack_template import IacStack

_ALLOWED_STAGES = frozenset({"dev", "homolog", "prod", "ci", "test"})


def resolve_stage() -> str:
    """
    STAGE preferencial; GITHUB_REF_NAME só como fallback.
    Normaliza para dev|homolog|prod|ci|test sem barras (evita refs de PR tipo N/merge).
    """
    raw = (os.environ.get("STAGE") or os.environ.get("GITHUB_REF_NAME") or "dev").strip().lower()
    # "123/merge", "infra/foo" → segmento seguro
    if "/" in raw:
        head, _, tail = raw.partition("/")
        if head in _ALLOWED_STAGES:
            return head
        if head == "infra":
            return "ci"
        if tail in _ALLOWED_STAGES:
            return tail
        return "ci"
    if raw in _ALLOWED_STAGES:
        return raw
    # branch feature / nome inválido → ci (seguro para synth; CD só roda em dev|homolog|prod)
    sanitized = re.sub(r"[^a-z0-9-]", "-", raw).strip("-") or "ci"
    return sanitized if sanitized in _ALLOWED_STAGES else "ci"


print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory()
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")
stage = resolve_stage()

tags = {
    # troque 'Template' pelo nome do seu MSS (obrigatório para o deployGuard)
    'project': 'Template',
    'stage': stage,
    'stack': stack_name,
    'owner': 'DevCommunity',
}

IacStack(
    app,
    stack_id=stack_name,
    stack_name=stack_name,
    stage=stage,
    env=cdk.Environment(
        account=aws_account_id,
        region=aws_region
        ),
    tags=tags
)

app.synth()
