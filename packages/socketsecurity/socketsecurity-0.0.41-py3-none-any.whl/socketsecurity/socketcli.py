import click
from core import Core, version
from core.classes import FullScanParams, Diff, Issue
from core.messages import Messages
import os


@click.command()
@click.option('--api_token', default='', help='The Socket API token can be set via SOCKET_SECURITY_API_KEY')
@click.option('--repo', default='', help='The name of the repository', required=True)
@click.option('--branch', default='main', help='The name of the branch')
@click.option('--committer', default='', help='The name of the person or bot running this', required=True)
@click.option('--pr_number', default='0', help='The pr or build number')
@click.option('--commit_message', default='', help='Commit or build message for the run')
@click.option('--default_branch', default=True, help='Whether this is the default/head for run')
@click.option('--target_path', default='./', help='Path to look for manifest files')
def cli(api_token, repo, branch, committer, pr_number, commit_message, default_branch, target_path):
    print(f"Starting Socket Security Scan version {version}")
    token = os.getenv("SOCKET_SECURITY_API_KEY") or api_token
    if token is None:
        print("Unable to get Socket Security API Token")
        exit(2)
    base_api_url = os.getenv("BASE_API_URL") or None
    core = Core(token=token, request_timeout=6000, base_api_url=base_api_url)
    set_as_pending_head = False
    if default_branch:
        set_as_pending_head = True
    params = FullScanParams(
        repo=repo,
        branch=branch,
        commit_message=commit_message,
        commit_hash="",
        pull_request=pr_number,
        committers=committer,
        make_default_branch=default_branch,
        set_as_pending_head=set_as_pending_head
    )
    diff: Diff
    diff = core.create_new_diff(target_path, params, workspace=target_path)
    security_comment = Messages.create_console_security_alert_table(diff)
    if len(diff.new_alerts) > 0:
        print("Security issues detected by Socket Security")
        print(security_comment)
        exit(1)
    else:
        print("No New wSecurity issues detected by Socket Security")


if __name__ == '__main__':
    cli()
