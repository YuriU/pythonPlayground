import boto3
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

@click.group()
def cli():
    """Shotty manages snapshots"""

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
        i.start()
    return

@instances.command('stop')
@click.option('--project', default=None)
def stop_instances(project):
    "Stop EC2 instances"

    for i in filter_instances(project):
        print("Stop {0} ...".format(i.id))
        i.stop()

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

if __name__ == '__main__':
    cli()