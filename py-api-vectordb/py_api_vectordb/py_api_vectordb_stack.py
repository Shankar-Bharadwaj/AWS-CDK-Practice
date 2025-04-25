from aws_cdk import (
    Stack,
    aws_apigateway,
    aws_lambda,
    aws_lambda_python_alpha
)
from constructs import Construct


# Get API_KEY from secrets.txt
def load_secrets(path):
    with open(path) as f:
        return dict(
            line.strip().split("=", 1) for line in f if "=" in line
        )


class PyApiVectordbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use AWS Secrets Manager for production-grade
        secrets = load_secrets("secrets.txt")

        # print(secrets) # {'API_KEY': 'pqqi35....'}

        # Defining the lambda
        # vector_lambda = aws_lambda.Function(
        #     self,
        #     "Vector-DB-Lambda",
        #     runtime=aws_lambda.Runtime.PYTHON_3_11,
        #     code=aws_lambda.Code.from_asset("services"),
        #     handler="index.handler",
        #     environment={
        #         "API_KEY": secrets.get("API_KEY", "")
        #     }
        # )


        # Defining lambda using aws_lambda_python_alpha since we have external dependencies
        vector_lambda = aws_lambda_python_alpha.PythonFunction(
            self,
            "Vector-DB-Lambda",
            entry="./services",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            index="index.py",
            handler="handler",
            environment={
                "API_KEY": secrets.get("API_KEY","")
            }
        )


        # Define API Gateway and the route
        api = aws_apigateway.RestApi(self, "Py-Vector-api")
        vector_resource = api.root.add_resource("vector")


        # Connecting the Lambda to our API Gateway
        vector_lambda_integration = aws_apigateway.LambdaIntegration(vector_lambda)
        vector_resource.add_method("POST", vector_lambda_integration)
        vector_resource.add_method("GET", vector_lambda_integration)
