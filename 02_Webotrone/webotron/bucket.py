# -*- coding: utf-8 -*-

"""Classes for S3 Buckets."""

import boto3
from botocore.exceptions import ClientError

class BucketManager:
    """Manages an S3 Bucket."""

    def __init__(self, session):
        """Create a BucketManager object"""
        self.s3 = session.resource('s3')
        pass

    def all_buckets(self):
        """Get an iterator for all buckets. """
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator to all bucket objects"""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Creates new or returns existing bucket"""
        
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.session.region_name
                    }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket)
            else:
                raise e

        return s3_bucket
    
    def set_policy(self, bucket):
        """Set bucket policy to be readable to anyone"""

        policy = """
        {
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::%s/*"
            ]
            }
        ]
        }
        """ % s3_bucket.name
        policy = policy.strip()

        pol = s3_bucket.Policy()
        pol.put(Policy=policy)

        ws = s3_bucket.Website()
        ws.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })