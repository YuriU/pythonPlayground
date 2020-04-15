# -*- coding: utf-8 -*-

"""Classes for Route53 domains."""

class DomainManager:
    """Manage a Route53 domain."""

    def __init__(self, session):
        self.session = session
        self.client = self.session.client('route53')


    def find_hosted_zone(self, domain_name):
        paginator = self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone

        return None



