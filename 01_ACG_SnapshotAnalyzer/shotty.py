import boto3
import botocore
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')


def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

def has_pending_snapshots(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@cli.group('instances')
def instances():
    """Commands for instances"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""


@instances.command('list')
@click.option('--project', default=None)
def list_instances(project):
    "List EC2 instances"
    for i in filter_instances(project):
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))
    return

@instances.command('start')
@click.option('--project', default=None)
def start_instances(project):
    "Start EC2 instances"

    for i in filter_instances(project):
        print("Starting {0} ...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0}.".format(i.id) + str(e))
            continue
    return

@instances.command('stop')
@click.option('--project', default=None)
def stop_instances(project):
    "Stop EC2 instances"

    for i in filter_instances(project):
        print("Stop {0} ...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0}.".format(i.id) + str(e))
            continue
    return

@instances.command('snapshot')
@click.option('--project', default=None)
def snapshot_instances(project):
    "Snapshot instances"
    for i in filter_instances(project):
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            if has_pending_snapshot(v):
                print("   Skipping {0}, snapshot already in progress".format(v.id))
                continue

            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshot analyzer")

        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()

    print("Job's done!")

    return

@volumes.command('list')
@click.option('--project', default=None)
def list_volumes(project):
    "List of volumes"
    for i in filter_instances(project):
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@snapshots.command('list')
@click.option('--project', default=None)
@click.option('--all', 'list_all', default=False, is_flag=True)
def list_snapshots(project, list_all):
    "List of Snapshots"
    for i in filter_instances(project):
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    v.state,
                    s.progress,
                    s.start_time.strftime("%C")
            )))

            if s.state == 'completed' and not list_all: break
    return

if __name__ == '__main__':
    cli()