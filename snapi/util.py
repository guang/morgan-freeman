import boto3
from settings import snapi_logger


s3 = boto3.resource('s3')
BUCKET_NAME = 'bwhoyouwant2-be-data'


def s3_to_local(key, local_path):
    s3.Bucket(BUCKET_NAME).download_file(key, local_path)
    snapi_logger.info("Downloaded file from '{remote}' to '{local_path}'".format(
        remote=BUCKET_NAME + key,
        local_path=local_path,
    ))


def data_to_s3(data, key):
    """ Upload source_file to given key on S3

    """
    new_store = s3.Object(BUCKET_NAME, key)
    snapi_logger.info("Uploading data to '{remote}'".format(
        remote=BUCKET_NAME + key,
    ))
    new_store.put(Body=data)


def allowed_file(filename):
    is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ('wav',)
    return is_allowed
