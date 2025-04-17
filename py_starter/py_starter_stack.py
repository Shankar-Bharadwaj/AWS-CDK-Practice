from aws_cdk import (
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput
)
from constructs import Construct

class PyStarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # s3 bucket construct where any file in it expires after 3 days
        bucket = s3.Bucket(self, "PyBucket",
            bucket_name = "mybucket1823919823u891e",
            lifecycle_rules = [
            s3.LifecycleRule(
                expiration = Duration.days(3)
            )
        ])

        # # To reproduce the error of 'resource already exists' due to the same physical ID (CDK IDs)
        # bucket = s3.Bucket(self, "PyBucketUpdated",
        #     bucket_name = "mybucket1823919823u891e"
        # )


        # Prints a placeholder value since 'cdk synth' doesn't deploy to AWS yet
        print("Bucket Name: ", bucket.bucket_name)  # Bucket Name:  ${Token[TOKEN.23]}


        # Outputting the bucket name using cdk
        CfnOutput(self, "PyBucketName",
                  value=bucket.bucket_name)
