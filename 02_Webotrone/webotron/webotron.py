#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Deploys websites with AWS

Webotrone automates the process of deploying static websites to AWS
- Configure AWS S3 buckets
- Create them
- Set them up for static website hosting
- Deploy local files to them
- Configure DNS with AWS Route53
- Configure a Content Delivery Network

"""

from pathlib import Path
import mimetypes

import boto3
from botocore.exceptions import ClientError
import click
from bucket import BucketManager


session = boto3.Session(profile_name='default')
bucket_manager = BucketManager(session)
s3 = session.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)
    return


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)
    return


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket"""

    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(bucket)

    return


def upload_file(s3_bucket, path, key):
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        }
    )


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync content of PATHNAME to BUCKET"

    s3_bucket = s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket,
                            str(p),
                            str(p.relative_to(root).as_posix()))

    handle_directory(root)

    pass


if __name__ == '__main__':
    cli()
