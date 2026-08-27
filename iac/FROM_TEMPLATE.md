# Do template ao seu MSS

Transição mínima: **só renomear identidade**. O template já resolve CI pin, `pytest` path, deps da layer e STAGE no CDK — sem steps bash extras no workflow.

## Checklist obrigatório (o `deployGuard` bloqueia se inalterado)

| O quê | Onde | Antes (template) | Depois (exemplo) |
|---|---|---|---|
| Nome do repositório | GitHub | `clean_mss_template` | `meu_mss` |
| Prefixo `STACK_NAME` | `.github/workflows/aws_deploy_cd.yml` | `CleanMssTemplateStack…` | `MeuMssStack…` |
| Tag `project` | `iac/app.py` | `'project': 'Template'` | `'project': 'MeuMss'` |

Validar localmente:

```bash
GITHUB_REPOSITORY=Maua-Dev/meu_mss bash .github/scripts/assert_project_configured.sh
```

## Recomendado (o guard emite `::warning::`, não falha)

| O quê | Onde | Antes | Depois (exemplo) |
|---|---|---|---|
| `path_part` da API (URL pública) | `iac/components/apigw_construct_template.py` | `template-mss` | `meu-mss` |
| `STACK_NAME` do synth CI | `.github/workflows/cdk_synth_ci.yml` | `CleanMssTemplateStackCi` | `MeuMssStackCi` |
| `MSS_NAME` | `.env.example` e/ou `cdk_synth_ci.yml` | `clean_mss_template` | `meu_mss` |

Não é necessário renomear classes/`*_template.py` no primeiro dia.

## Fluxo

1. Renomear o repo (≠ `clean_mss_template`).
2. Trocar prefixo `STACK_NAME` no CD.
3. Trocar tag `project` em `iac/app.py`.
4. Trocar `path_part` do API Gateway.
5. (Opcional) alinhar `MSS_NAME` / synth CI / README.
6. Configurar vars/secrets do GitHub uma vez (abaixo).
7. Push em `dev` → CD sobe.

## GitHub — Environments, vars e secrets

Crie Environments: `dev`, `homolog`, `prod`.

**Vars** (repository ou environment):

- `AWS_REGION` (ex. `sa-east-1`)
- `GRAPH_MICROSOFT_ENDPOINT` (ex. `https://graph.microsoft.com/v1.0/me`)

**Secrets** (org ou repo):

- `AWS_ACCOUNT_ID_DEV`
- `AWS_ACCOUNT_ID_HOML`
- `AWS_ACCOUNT_ID_PROD`

A role OIDC `GithubActionsRole` precisa existir em cada account.

## O que o template já resolve sozinho

- CI reusable: `pytest_ci_313.yml@V1.3`
- `pytest.ini` com `pythonpath = .` (import `src` no pytest 8)
- Layer com `aws_xray_sdk` + `boto3` (authorizer / ObservabilityAWS)
- `STAGE` normalizado em `iac/app.py` (`STAGE` preferencial; sem step “Resolve STAGE”)
- `cdk_synth_ci.yml` usa `STAGE=ci` fixo; synth **não** roda em `pull_request`

## Token Microsoft (Graph)

Use audience do Graph, não cole JWT em issues/chat:

```bash
az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv
```

## Local

```bash
cp .env.example .env   # STAGE=TEST
pip install -r requirements-dev.txt
PYTHONPATH=. pytest    # ou só pytest (pytest.ini já define pythonpath)
```
