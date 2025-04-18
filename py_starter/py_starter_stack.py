from aws_cdk import (
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    Fn
)
from constructs import Construct


class PyStarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        suffix = self.__initialize_suffix()

        # s3 bucket construct where any file in it expires after 3 days
        bucket = s3.Bucket(self, "PyBucket",
            bucket_name = f"cool-bucket-{suffix}",
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


    def __initialize_suffix(self):
        """
        Using CloudFormation intrinsic functions to get the suffix of stack_id. Stack_id is a 
        CDK Token (a placeholder) till it gets deployed on AWS. Its not a real string at synth time. 
        Hence, we can not use normal python functions like split and slicing to get the suffix.

        This example shows us how we can use intrinsic functions to deal with properties/objects 
        that are not available at runtime.
        """

        short_stack_id = Fn.select(2, Fn.split('/', self.stack_id))
        suffix = Fn.select(3, Fn.split('-', short_stack_id))
        return suffix
