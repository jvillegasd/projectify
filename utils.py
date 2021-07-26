import os
import boto3
from environs import Env
from constants import UPLOAD_FOLDER
from botocore.exceptions import ClientError

env = Env()
env.read_env()

def upload_file_to_s3(filename, bucket=None, object_name=None):
  if not object_name:
    object_name = filename
  if not bucket:
    bucket = env('BUCKETEER_BUCKET_NAME')
  
  s3_client = boto3.client(
    service_name='s3',
    region_name=env('BUCKETEER_AWS_REGION'),
    aws_access_key_id=env('BUCKETEER_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('BUCKETEER_AWS_SECRET_ACCESS_KEY')
  )
  try:
    path = os.path.join(UPLOAD_FOLDER, object_name)
    response = s3_client.upload_file(path, bucket, object_name)
  except ClientError as e:
    print(e, flush=True)
    return False
  return True

def upload_fileobj_to_s3(file, filename, bucket=None, object_name=None):
  if not object_name:
    object_name = filename
  if not bucket:
    bucket = env('BUCKETEER_BUCKET_NAME')
  
  s3_client = boto3.client(
    service_name='s3',
    region_name=env('BUCKETEER_AWS_REGION'),
    aws_access_key_id=env('BUCKETEER_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('BUCKETEER_AWS_SECRET_ACCESS_KEY')
  )
  try:
    path = os.path.join(UPLOAD_FOLDER, object_name)
    response = s3_client.upload_fileobj(file, bucket, object_name)
  except ClientError as e:
    print(e, flush=True)
    return False
  return True

def download_file_from_s3(filename, bucket=None, object_name=None):
  if not object_name:
    object_name = filename
  if not bucket:
    bucket = env('BUCKETEER_BUCKET_NAME')
  
  s3_client = boto3.client(
    service_name='s3',
    region_name=env('BUCKETEER_AWS_REGION'),
    aws_access_key_id=env('BUCKETEER_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('BUCKETEER_AWS_SECRET_ACCESS_KEY')
  )
  try:
    path = os.path.join(UPLOAD_FOLDER, object_name)
    response = s3_client.download_file(bucket, object_name, path)
  except ClientError as e:
    print(e, flush=True)
    return False
  return True

def create_presigned_url_s3(object_name, bucket=None, expiration_seg=3600):
  if not bucket:
    bucket = env('BUCKETEER_BUCKET_NAME')
  
  s3_client = boto3.client(
    service_name='s3',
    region_name=env('BUCKETEER_AWS_REGION'),
    aws_access_key_id=env('BUCKETEER_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('BUCKETEER_AWS_SECRET_ACCESS_KEY')
  )
  try:
    response = s3_client.generate_presigned_url(
      'get_object',
      Params={
        'Bucket': bucket,
        'Key': object_name
      },
      ExpiresIn=expiration_seg
    )
  except ClientError as e:
    print(e, flush=True)
    return None
  
  return response

def delete_file(filename):
  path = os.path.join(UPLOAD_FOLDER, filename)
  os.remove(path)