from time import sleep
from prefect_aws import S3Bucket, AwsCredentials
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)


def create_aws_creds_block():
    my_aws_creds_obj = AwsCredentials(
        aws_access_key_id=os.environ["ROOT_USER_ACCESS_KEY"],
        aws_secret_access_key=os.environ["ROOT_USER_SECRET_ACCESS_KEY"],
        aws_session_token=None,
        region_name="us-east-1"
    )
    my_aws_creds_obj.save(name="my-aws-creds", overwrite=True)


def create_s3_bucket_block():
    aws_creds = AwsCredentials.load("my-aws-creds")
    my_s3_bucket_obj = S3Bucket(
        bucket_name=os.environ["MLFOW_S3_BUCKET"], credentials=aws_creds
    )
    my_s3_bucket_obj.save(name="s3-bucket-example", overwrite=True)


if __name__ == "__main__":
    create_aws_creds_block()
    sleep(5)
    create_s3_bucket_block()
