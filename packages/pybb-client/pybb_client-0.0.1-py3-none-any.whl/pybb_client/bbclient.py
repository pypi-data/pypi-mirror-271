#!python3

import requests as req

from atlassian import Bitbucket
from requests.auth import HTTPBasicAuth


class BbClient:

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.dashboard_url = f'{base_url}/rest/api/latest/dashboard'
        self.pull_requests_url = f'{self.dashboard_url}/pull-requests'
        self.username = username
        self.password = password
        self.client = Bitbucket(
            url=base_url,
            username=username,
            password=password,
        )

    def list_assigned_pull_requests(self):
        pr_list_res = req.get(
            url=self.pull_requests_url,
            auth=HTTPBasicAuth(self.username, self.password),
            verify=False,
            params={
                'role': 'REVIEWER',
                'state': 'OPEN',
                'participantStatus': 'UNAPPROVED',
            },
        )
        if pr_list_res.status_code != 200:
            raise Exception('Failed to list assigned PRs')
        pr_list_json = pr_list_res.json()
        pr_list = pr_list_json['values']
        return pr_list


def lol():
    pass