#!/usr/bin/env python3

from aws_cdk import core

from scheduler_api_template_py.scheduler_api_template_py_stack import SchedulerApiTemplatePyStack


app = core.App()
SchedulerApiTemplatePyStack(app, "scheduler-api-template-py")

app.synth()
