# How to test the local IaC

## Prerequisites
- have docker installed and running
- have [sam](https://docs.aws.amazon.com/serverless-application-model/index.html) installed

## Setup dynamodb local
- `docker run -p 8000:8000 amazon/dynamodb-local -sharedDB -inMemory`
- run `src/shared/infra/repositories/load_user_mock_to_dynamo.py`


## Build cdk (/iac)
- `cdk synth`
- `sam build -t ./cdk.out/IacStack.template.json`
- `sam local start-api -t ./cdk.out/IacStack.template.json`
- 
