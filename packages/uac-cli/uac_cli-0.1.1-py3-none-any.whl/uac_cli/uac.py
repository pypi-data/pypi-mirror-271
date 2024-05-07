from dotenv import load_dotenv
import os
import sys
import logging
import uac_api
import click
import uac_api.payload
from . import __version__
from utils.process import process_output, process_input, create_payload


# Load environment variables from .env file
load_dotenv()

__output = None
__select = None
output_option = click.option('--output', '-o', type=click.File('w'))
output_option_binary = click.option('--output', '-o', type=click.File('wb'))
select_option = click.option('--select', '-s', help="select which field to be returned. JSONPATH")
input_option = click.option('--input', '-i', type=click.File('r'))
ignore_ids = click.option("--ignore-ids/--no-ignore-ids", "-ig/-nig", is_flag=True, default=True, help="Ignore sysIDs in the payload")

class UacCli:
    def __init__(self, log_level):
        self.log_level = log_level

    def main(self):
        if self.log_level != "DEBUG":
            sys.tracebacklimit = 0
        logging.basicConfig(level=self.log_level)
        logging.info(f'UAC CLI is running... ({__version__})')
        self.log = logging
        self.config = self.get_config()
        self.uac = uac_api.UniversalController(base_url=self.config["uac_url"], token=self.config["token"], logger=self.log)
        self.log.info(f'UAC URL: {self.config["uac_url"]}')
        
        return self.uac

    def get_config(self):
        config = {
            "uac_url": os.getenv('UAC_URL'),
            "token": os.getenv('UAC_TOKEN'),
        }
        return config
    
@click.group()
@click.version_option(version=__version__)
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), default='ERROR')
@click.pass_context
def main(ctx, log_level):
    cli = UacCli(log_level=log_level)
    ctx.obj = cli.main()







































main.add_command(agents.get_agent_cluster)
main.add_command
def agent_cluster():
def agent():
def get_agent_cluster(uac, args, output=None, select=None):
def update_agent_cluster(uac, args, output=None, input=None, select=None):
def create_agent_cluster(uac, args, output=None, input=None, select=None, ignore_ids=False):
def delete_agent_cluster(uac, args, output=None, select=None):
def list_agent_clusters(uac, args, output=None, select=None):
def list_agent_clusters_advanced(uac, args, output=None, select=None):
def get_selected_agent(uac, args, output=None, select=None):
def resolve_cluster(uac, args, output=None, select=None):
def resume_cluster(uac, args, output=None, select=None):
def set_cluster_task_execution_limit(uac, args, output=None, select=None):
def suspend_cluster(uac, args, output=None, select=None):
def get_agent(uac, args, output=None, select=None):
def update_agent(uac, args, output=None, input=None, select=None):
def delete_agent(uac, args, output=None, select=None):
def list_agents(uac, args, output=None, select=None):
def list_agents_advanced(uac, args, output=None, select=None):
def resume_agent(uac, args, output=None, select=None):
def resume_agent_cluster_membership(uac, args, output=None, select=None):
def set_agent_task_execution_limit(uac, args, output=None, select=None):
def suspend_agent(uac, args, output=None, select=None):
def suspend_agent_cluster_membership(uac, args, output=None, select=None):











# @promote.command('promote_1', short_help='Promotes, without a bundle, one or more items of a specific type.')
# @click.argument('args', nargs=-1, metavar='item_type=value item_ids=value item_names=value items=value promotion_target_id=value promotion_target_name=value override_user=value override_password=value exclude_on_existence=value follow_references=value allow_unv_tmplt_changes=value override_token=value')
# @click.pass_obj
# @output_option
# @select_option
# def promote_1(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.promotes.promote_1(**vars_dict)
#     process_output(output, select, response)



# @snmpmanager.command('get', short_help='None')
# @click.argument('args', nargs=-1, metavar='managerid=value managername=value')
# @click.pass_obj
# @output_option
# @select_option
# def get_snmp_connection(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.snmpmanagers.get_snmp_connection(**vars_dict)
#     process_output(output, select, response)


# @snmpmanager.command('update', short_help='None')
# @click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value manager_address=value manager_port=value retain_sys_ids=value opswise_groups=value trap_community=value description=value')
# @click.pass_obj
# @output_option
# @select_option
# @input_option
# def update_snmp_connection(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.snmpmanagers.update_snmp_connection(**vars_dict)
#     process_output(output, select, response)


# @snmpmanager.command('create', short_help='None')
# @click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
# @click.pass_obj
# @output_option
# @select_option
# @input_option
# def create_snmp_connection(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.snmpmanagers.create_snmp_connection(**vars_dict)
#     process_output(output, select, response)


# @snmpmanager.command('delete', short_help='None')
# @click.argument('args', nargs=-1, metavar='managerid=value managername=value')
# @click.pass_obj
# @output_option
# @select_option
# def delete_snmp_connection(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.snmpmanagers.delete_snmp_connection(**vars_dict)
#     process_output(output, select, response)


# @snmpmanager.command('list', short_help='None')
# @click.argument('args', nargs=-1, metavar='')
# @click.pass_obj
# @output_option
# @select_option
# def list_snmp_connections(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.snmpmanagers.list_snmp_connections(**vars_dict)
#     process_output(output, select, response)




def run():
    main()

if __name__ == '__main__':
    main()