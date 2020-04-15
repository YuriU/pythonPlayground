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

import boto3
import click
from bucket import BucketManager


session = None
bucket_manager = None


@click.group()
@click.option('--profile', default=None,
    help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS"""

    global session, bucket_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)

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
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync content of PATHNAME to BUCKET"

    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))
    pass


if __name__ == '__main__':
    cli()
