#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.template_stack import TemplateStack


app = cdk.App()
TemplateStack(app, "IacStack", env={'region': 'us-east-2'})

app.synth()
