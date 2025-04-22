import aws_cdk as core
import aws_cdk.assertions as assertions

from py_api_vectordb.py_api_vectordb_stack import PyApiVectordbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in py_api_vectordb/py_api_vectordb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PyApiVectordbStack(app, "py-api-vectordb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
