# How to test the local IaC

## Prerequisites
- have docker installed and running
- have [sam](https://docs.aws.amazon.com/serverless-application-model/index.html) installed

## Setup dynamodb local
- `docker run -p 8000:8000 amazon/dynamodb-local -sharedDB -inMemory`
- seed local: `python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target local`
- seed AWS DEV/HOMOLOG (after cdk deploy): `python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target aws` (set STAGE + Dynamo env vars; blocked on PROD)


## Build cdk (/iac)
- `cdk synth`
- `sam build -t ./cdk.out/IacStack.template.json`
- `sam local start-api -t ./cdk.out/IacStack.template.json`
- 
