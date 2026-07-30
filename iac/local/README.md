# How to test the local IaC

## Prerequisites
- have docker installed and running
- have [sam](https://docs.aws.amazon.com/serverless-application-model/index.html) installed

## Start local services (DynamoDB + MinIO)

From `iac/local`:

```bash
docker compose up -d
```

| Service | URL / port | Notes |
|---------|------------|--------|
| DynamoDB Local | `http://localhost:8000` | persistence in `./docker/dynamodb` |
| MinIO S3 API | `http://localhost:9000` | credentials `minioadmin` / `minioadmin` |
| MinIO Console | http://localhost:9001 | web UI |

On first boot, `minio-init` creates the bucket `template_bucket1_name` (same name as `Environments.s3_template_bucket1_name` in `STAGE=TEST`).

### Seed DynamoDB
- local: `python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target local`
- AWS DEV/HOMOLOG (after cdk deploy): `python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target aws` (set STAGE + Dynamo env vars; blocked on PROD)

### Integration tests (DynamoDB Local)
Os testes `test_*_repository_dynamo.py` estão com `@pytest.mark.skip(reason="Needs dynamoDB")` — **não rodam no CI**.

Para rodar localmente: suba o Docker, rode o seed, remova o `skip` do teste e execute o pytest normalmente. Sem Dynamo up, o teste falha.

### Point boto3 / code at MinIO (example)

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1",
)
s3.list_objects_v2(Bucket="template_bucket1_name")
```

## Build cdk (/iac)
- `cdk synth`
- `sam build -t ./cdk.out/IacStack.template.json`
- `sam local start-api -t ./cdk.out/IacStack.template.json`
