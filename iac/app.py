#!/usr/bin/env python3
import os

import aws_cdk as cdk
from adjust_layer_directory import adjust_layer_directory

from iac.template_stack import TemplateStack



print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory(shared_dir_name="shared", destination="lambda_layer_out_temp")
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")

if 'prod' in stack_name:
    stage = 'PROD'

elif 'homolog' in stack_name:
    stage = 'HOMOLOG'

elif 'dev' in stack_name:
    stage = 'DEV'

else:
    stage = 'TEST'

tags = {
    'project': 'Template',
    'stage': stage,
    'stack': 'BACK',
    'owner': 'DevCommunity'
}

TemplateStack(app, stack_name=stack_name, env=cdk.Environment(account=aws_account_id, region=aws_region), tags=tags)


app.synth()
