import boto3
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

@click.group()
def instances():
    """Commands for instances"""


@instances.command('list')
@click.option('--project', default=None)
def list_instances(project):
    "List EC2 instances"

    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    
    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvaliabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))
    return

if __name__ == '__main__':
    instances()