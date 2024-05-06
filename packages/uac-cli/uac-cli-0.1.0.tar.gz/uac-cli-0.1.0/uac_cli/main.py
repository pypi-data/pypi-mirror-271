from dotenv import load_dotenv
import os
from pathlib import Path
import sys
import logging
import uac_api
import click
import yaml
import uac_api.payload
from . import __version__


from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids
from uac_cli.utils.config import write_config, read_config, ask_profile, read_profile, write_profile
from uac_cli.commands.agent import agent
from uac_cli.commands.agent_cluster import agent_cluster
from uac_cli.commands.audit import audit
from uac_cli.commands.bundle import bundle, promotion, promotion_target
from uac_cli.commands.business_service import business_service
from uac_cli.commands.calendar import calendar
from uac_cli.commands.cluster_node import cluster_node
from uac_cli.commands.connection import connection
from uac_cli.commands.credential import credential
from uac_cli.commands.custom_day import custom_day
from uac_cli.commands.email_template import email_template
from uac_cli.commands.ldap import ldap
from uac_cli.commands.metric import metrics
from uac_cli.commands.oauth_client import oauth_client
from uac_cli.commands.oms_server import oms_server
from uac_cli.commands.property import property
from uac_cli.commands.report import report
from uac_cli.commands.script import script
from uac_cli.commands.server_operation import server_operation
from uac_cli.commands.simulation import simulation
from uac_cli.commands.system import system
from uac_cli.commands.task import task
from uac_cli.commands.task_instance import task_instance
from uac_cli.commands.trigger import trigger
from uac_cli.commands.universal_event import universal_event
from uac_cli.commands.universal_event_template import universal_event_template
from uac_cli.commands.universal_template import universal_template
from uac_cli.commands.user import user
from uac_cli.commands.user_group import user_group
from uac_cli.commands.variable import variable
from uac_cli.commands.virtual_resource import virtual_resource
from uac_cli.commands.webhook import webhook
from uac_cli.commands.workflow import workflow
from uac_cli.commands.config import config



# Load environment variables from .env file
load_dotenv()

__output = None
__select = None


class UacCli:
    def __init__(self, profile_name='default', log_level='ERROR'):
        self.log_level = log_level
        self.profile = read_profile(profile_name)
        self.setup_logging()

    def setup_logging(self):
        if self.log_level != "DEBUG":
            sys.tracebacklimit = 0
        logging.basicConfig(level=self.log_level)
        logging.info(f'UAC CLI is running... (Version: {__version__})')
        self.log = logging
    
    def main(self):
        if not self.profile:
            return None

        if self.profile.get('token', None):
            self.uac = uac_api.UniversalController(base_url=self.profile["url"], token=self.profile["token"], logger=self.log)
        else:
            self.uac = uac_api.UniversalController(base_url=self.profile["url"], credential=(self.profile.get('username'), self.profile.get('password')), logger=self.log)
        self.log.info(f'UAC URL: {self.profile["url"]}')
        
        return self.uac
    

@click.group()
@click.version_option(version=__version__)
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), default='ERROR')
@click.option('--profile', '-p', help="Profile to use for the CLI. The profiles must be added to ~/.uac/profiles.yml", default="default")
@click.pass_context
def main(ctx, log_level, profile):
    cli = UacCli(log_level=log_level, profile_name=profile)
    ctx.obj = cli.main()


main.add_command(config)
main.add_command(agent)
main.add_command(agent_cluster)
main.add_command(audit)
main.add_command(bundle)
main.add_command(business_service)
main.add_command(calendar)
main.add_command(cluster_node)
main.add_command(connection)
main.add_command(credential)
main.add_command(custom_day)
main.add_command(email_template)
main.add_command(ldap)
main.add_command(metrics)
main.add_command(oauth_client)
main.add_command(oms_server)
main.add_command(property)
main.add_command(report)
main.add_command(script)
main.add_command(server_operation)
main.add_command(simulation)
main.add_command(system)
main.add_command(task)
main.add_command(task_instance)
main.add_command(trigger)
main.add_command(universal_event)
main.add_command(universal_event_template)
main.add_command(universal_template)
main.add_command(user)
main.add_command(user_group)
main.add_command(variable)
main.add_command(virtual_resource)
main.add_command(webhook)
main.add_command(workflow)
main.add_command(promotion)
main.add_command(promotion_target)

def run():
    main()

if __name__ == '__main__':
    main()