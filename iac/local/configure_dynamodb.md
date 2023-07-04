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

## Running the `load_user_mock_to_dynamo` Script

Finally, you can run the `load_user_mock_to_dynamo` script to load mock data into DynamoDB. Follow the steps below:

1. Locate the directory or file named `load_user_mock_to_dynamo` within your project. This directory or file is responsible for loading mock data into DynamoDB
2. If the `load_user_mock_to_dynamo` file doesn't exist, you need to create it.
3. Once you have located or created the `load_user_mock_to_dynamo` file, make sure it is in the correct location within your project structure. The file should be located in the `src/shared/infra/repositories`
```bash
.
├── iac
├── src
│   ├── ...
│   │     
│   │    
│   └── shared
│       ├── domain
│       │   └── ...
│       │   
│       ├── helpers
│       │   └── ...
│       │   
│       └── infra
│           ├── dto
│           ├── external
│           └── repositories
│               └── -> [load_user_mock_to_dynamo] <-
...
```
4. This file is responsible for populating DynamoDB with mock data
5. Then, make sure you are in the root directory of your project again
6. Run the following command to execute the script:
   ```
   py -m src.shared.infra.repositories.load_user_mock_to_dynamo
   ```


This command will run the `load_user_mock_to_dynamo` script and populate DynamoDB with the provided mock data

## Launch NoSQL WorkBench

Lastly, you need to set NoSQL WorkBench to receive and visualize data runned. Follow the steps below:

1. Launch DynamoDB
2. Open Operation builder and add a connection
3. Select DynamoDB Local
4. Open Local