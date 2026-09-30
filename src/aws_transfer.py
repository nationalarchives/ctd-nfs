import os
from collections.abc import Generator

import boto3
from botocore.exceptions import ClientError

from src._tools.constants import PATH
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error(e)
        return False
    return True
           
            
def get_candidate_files() -> Generator:
    for json_file in PATH.PUBLISH.rglob("*.json"):
        print(json_file)
        yield json_file


def main():
    logger.info(" ===== UPLOADING JSONs ===== ")
    candidate_files = get_candidate_files()


if __name__ == "__main__":
    main()

