#!/usr/bin/env python3
import os

import aws_cdk as cdk

from py_starter.py_starter_stack import PyStarterStack
from py_starter.py_handler_stack import PyHandlerStack


app = cdk.App()

starter_stack = PyStarterStack(app, "PyStarterStack")

# Passing a bucket from one stack to the other in the form of constructor parameter
PyHandlerStack(app, "PyHandlerStack", starter_stack.get_bucket)

app.synth()
