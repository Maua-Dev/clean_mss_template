# DynamoDB Setup Guide

This guide will walk you through the steps to set up DynamoDB on your local machine using Docker and configure it for your project.

## Installation (Only first time)

Before getting started, make sure you have the following installed on your machine:

- Docker: (https://docs.docker.com/desktop/install/windows-install/)
- NoSQL Workbench: (https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)
- AWS CLI: (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### AWS Settings

To interact with DynamoDB, you need to set up your AWS credentials. Follow the steps below to configure your credentials:

1. Open a terminal on your machine
2. Run the following command to configure your AWS credentials:
```
    aws configure
```
3. Enter your AWS Access Key ID and Secret Access Key when apper. These can be anything you want but empty
4. Set the Default region name to `sa-east-1`
5. Set the Default output format to `json`
```
    AWS Access Key ID: demo
    AWS Secret Access Key: demo
    Default region name: sa-east-1
    Default output format: json
```

### Docker Settings

Next, you need to configure DynamoDB for your project and Docker compose. Follow the steps below:

1. Open a terminal and navigate to your project directory
2. Then, prompt the following commands:
```
    cd iac
    cd local
    docker-compose up -d
```

### Create virtual enviroments in python (once for project)

###### Windows

    python -m venv venv

###### Linux

    virtualenv -p python3.9 venv

### Activate the venv

###### Windows:

    venv\Scripts\activate

###### Linux:

    source venv/bin/activate

### Install the requirements

    pip install -r requirements-dev.txt

### Configure Environment Variables

Create a file named `.env` in the root directory and add the following line to the file:
```
    STAGE=TEST
```

## Launch DynamoDB in Docker 

Start the DynamoDB Local container using Docker:

1. Open Docker
2. Start dynamodb-local container

## Running the `load_item_mock_to_dynamo` Script

Seed mock `Item` data into DynamoDB. Two targets:

### Local (DynamoDB Local / Docker)

Creates the table (with GSI) if missing, then loads mock items:

```bash
# from repo root, with STAGE=TEST (default)
python -m src.shared.infra.repositories.load_item_mock_to_dynamo
# or explicitly:
python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target local
```

### AWS DEV / HOMOLOG (manual, after CDK deploy)

Does **not** create the table — CDK already did. Only seeds data. Refuses `PROD`.

```bash
STAGE=DEV \
REGION=sa-east-1 \
DYNAMO_TABLE_NAME=TemplateTable1-dev \
DYNAMO_PARTITION_KEY=pk \
DYNAMO_SORT_KEY=sk \
python -m src.shared.infra.repositories.load_item_mock_to_dynamo --target aws
```

Use your real table name / region from the deployed stack. Do not run this against production.

The script file lives at:

```bash
src/shared/infra/repositories/load_item_mock_to_dynamo.py
```

## Launch NoSQL WorkBench

Lastly, you need to set NoSQL WorkBench to receive and visualize data runned. Follow the steps below:

1. Launch DynamoDB
2. Open Operation builder and add a connection
3. Select DynamoDB Local
4. Open Local