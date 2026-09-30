import os
from collections.abc import Generator
from pathlib import Path
from typing import Literal

import boto3
from botocore.exceptions import ClientError

from src._tools.constants import PATH
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


Prefix = Literal['jsons-to-process', 'jsons-to-validate']


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
           
            
def convert_file_name_to_bucket_name(candidate_file: Path, prefix: Prefix) -> str:
    publish_path = candidate_file.relative_to(PATH.PUBLISH)
    county = publish_path.parents[2].name
    version = publish_path.parents[0].name
    json = publish_path.name
    return f"{prefix}/{county}/{version}/{json}"


def get_candidate_files() -> Generator:
    for json_file in PATH.PUBLISH.rglob("*.json"):
        print(json_file)
        yield convert_file_name_to_bucket_name(json_file)


def main():
    logger.info(" ===== UPLOADING JSONs ===== ")
    candidate_files = get_candidate_files()


if __name__ == "__main__":
    main()

