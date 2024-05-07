"""AWS related functions"""
from __future__ import absolute_import

import json
import logging
from typing import Union

import boto3
import psycopg2


logger = logging.getLogger(__name__)


def connect_rds(
        secret_id: str,
        db_name: str = None,
        commit: bool = False,
        **kwargs
) -> psycopg2.extensions.connection:
    """Create a connector to an AWS RDS database.

    It will search the secret into Secrets Manager to retreive all the connection informations.
    The only parameter not retreive is the database name in the server it will connect to but you
    can provide it as an argument.

    If you don't enter one, the default postgres behaviour is applied : the username is used as
    database name.
    (see https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS)

    As this is just a wrapper around the `psycopg2.connect` please refer to the doc if you need
    description on the other parameter you can pass.
    (see https://www.psycopg.org/docs/module.html#psycopg2.connect)

    Args:
        secret_id (str): The name of the secret for the database in Secret Manager
        db_name (str): The name of the db to connect to. Default to None.
        commit (bool): Flag to specify if you want to enable the autocommit on the connector.
            Default to False.

    Raises:
        secret_unknown: The secret entered as parameter is not known in Secret Manager

    Returns:
        psycopg2.extensions.connection: The connector to the database
    """
    secrets = boto3.client('secretsmanager', 'eu-west-1')

    try:
        credentials = json.loads(secrets.get_secret_value(SecretId=secret_id).get('SecretString'))
    except secrets.exceptions.ResourceNotFoundException as secret_unknown:
        logger.exception('Secret: %s not found !', secret_id)
        raise secret_unknown

    connector = psycopg2.connect(
        user=credentials.get('username'),
        password=credentials.get('password'),
        port=credentials.get('port'),
        dbname=db_name if db_name else credentials.get('username'),
        host=credentials.get('host'),
        **kwargs
    )

    if commit:
        connector.set_session(autocommit=True)

    return connector


def s3_to_memory(bucket: str, file_key: str, decode_utf: bool = False) -> Union[str, bytes]:
    """Download the content of a file from s3 into memory

    Args:
        bucket (str): The bucket name where the file is located
        file_key (str): The complete file key of the file inside the bucket

    Returns:
        Union[str, bytes]: The content of the file as a string of a bytes array depending on the
            file.
    """
    s3_client = boto3.client('s3')

    response = s3_client.get_object(Bucket=bucket, Key=file_key)

    if decode_utf:
        return response['Body'].read().decode('utf-8')

    return response['Body'].read()


def upload_to_s3(bucket: str, file_key: str) -> None:
    pass
