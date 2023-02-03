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
TemplateStack(app, "IacStack", env={'region': 'us-east-2'})

app.synth()
