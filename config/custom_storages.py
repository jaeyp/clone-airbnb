from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static/"  # default: location = setting('AWS_LOCATION', '')
    file_overwrite = False  # skip upload if there is same file


class UploadStorage(S3Boto3Storage):
    location = "uploads/"
