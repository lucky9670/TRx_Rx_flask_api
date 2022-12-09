import logging
import boto3
from botocore.exceptions import ClientError
import uuid
#import json

bucket_name='dataconnecxion-customers-csv'
s3Obj = None

def set_boto3_conn():
    global s3Obj
    try:
        s3Obj = boto3.client('s3',
                        region_name='us-east-2',
                        aws_access_key_id='AKIA5VEY5YWKMMRN3H27',
                        aws_secret_access_key='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')
        return 0
    except Exception as e:
        print(e)
        return 1

def get_boto3_conn():
    global s3Obj
    try:
        if not s3Obj:
            return set_boto3_conn()
            
        return 0
    except Exception as e:
        print(e)
        return set_boto3_conn()



class s3_file():
    def __init__(self,file,key):
        self.object=file
        self.object_key = key
        self.bucket = None #DEFINE BUCKET NAME FOR EVERYCLASS WITHIN THE FUNCTION

    def put_img_before(self):
        if get_boto3_conn():
            return {"err":'Could not upload image'}

        try:

            self.bucket = 'dataconnecxion-customers-csv'

            s3Obj.put_object(
                Body = self.object,
                Bucket = self.bucket,
                Key = self.object_key,
                ContentType = self.object.content_type
                )
            return {'object_key':self.object_key}

        except Exception as e:
            print(e)
            return {'err':"Unexpected Error uploading Image"}


print(get_boto3_conn(),'S3 client connection initialized')