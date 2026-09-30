import os
import tomllib
from collections.abc import Generator
from pathlib import Path
from typing import Literal

import boto3
from botocore.exceptions import ClientError

from src._tools.constants import PATH
from src._tools.logging_setup import create_logger

logger = create_logger("src._config", "logging.yaml")


Prefix = Literal['jsons-to-process', 'jsons-to-validate']


def upload_files(candidate_files: Generator, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3')
    with open(Path(r"src/run_options.toml"), mode="rb") as fp:
        config = tomllib.load(fp)

    for _file in candidate_files:
        object_name = convert_file_name_to_object_name(_file, config['transfer']['prefix'])

        try:
            s3_client.upload_file(_file, bucket, object_name)
        except ClientError as e:
            logger.error(e)
            return False
        return True
           
            
def convert_file_name_to_object_name(candidate_file: Path, prefix: Prefix) -> str:
    publish_path = candidate_file.relative_to(PATH.PUBLISH)
    county = publish_path.parents[2].name
    version = publish_path.parents[0].name
    json = publish_path.name
    return f"{prefix}/{county}/{version}/{json}"


def get_candidate_files() -> Generator:
    for json_file in PATH.PUBLISH.rglob("*.json"):
        yield from json_file


def main():
    logger.info(" ===== UPLOADING JSONs ===== ")

    candidate_files = get_candidate_files()


if __name__ == "__main__":
    main()

