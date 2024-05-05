from pybb_client import bbclient as bbc


def test_list_assigned_pull_requests_not_empty():
    bbclient = bbc.BbClient(
        base_url='https://git.moscow.alfaintra.net',
        username='U_02796',
        password='nZthR9EcVxZK',
    )
    prs = bbclient.list_assigned_pull_requests()
    assert len(prs) > 0