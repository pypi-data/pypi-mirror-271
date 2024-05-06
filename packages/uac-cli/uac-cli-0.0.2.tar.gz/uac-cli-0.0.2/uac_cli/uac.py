from dotenv import load_dotenv
import os
import sys
import logging
import uac_api
import click
import uac_api.payload
from . import __version__
from .utils import process_output, process_input, create_payload

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

# Audits

@main.group()
def audit():
    pass

@main.group()
def agent_cluster():
    pass

@main.group()
def agent():
    pass

@main.group()
def bundle():
    pass

@main.group()
def business_service():
    pass

@main.group()
def calendar():
    pass

@main.group()
def cluster_node():
    pass

@main.group()
def credential():
    pass

@main.group()
def custom_day():
    pass

@main.group()
def connection():
    pass

@connection.group()
def database():
    pass

@connection.group()
def email():
    pass

@main.group()
def email_template():
    pass

@main.group()
def ldap():
    pass

@main.group()
def metrics():
    pass

@main.group()
def oauth_client():
    pass

@main.group()
def oms_server():
    pass

@connection.group()
def peoplesoft():
    pass

# @main.group()
# def promote():
#     pass

@main.group()
def promotion():
    pass

@main.group()
def promotion_target():
    pass

@main.group()
def property():
    pass

@main.group()
def report():
    pass

@connection.group()
def sap():
    pass

@main.group()
def script():
    pass

@main.group()
def server_operation():
    pass

@main.group()
def simulation():
    pass

# @main.group()
# def snmpmanager():
#     pass

@main.group()
def system():
    pass

@main.group()
def task_instance():
    pass

@main.group()
def task():
    pass

@main.group()
def trigger():
    pass

@main.group()
def universal_event():
    pass

@main.group()
def universal_event_template():
    pass

@main.group()
def universal_template():
    pass

@main.group()
def user_group():
    pass

@main.group()
def user():
    pass

@main.group()
def variable():
    pass

@main.group()
def virtual_resource():
    pass

@main.group()
def webhook():
    pass

@main.group()
def workflow():
    pass


# - auditType: auditType 
# - source: source 
# - status: status 
# - createdBy: createdBy 
# - tableName: tableName 
# - tableRecordName: tableRecordName 
# - updatedTimeType: updatedTimeType 
# - updatedTime: updatedTime 
# - tableKey: tableKey 
# - includeChildAudits: includeChildAudits 
@audit.command('list', short_help='Get a list of audits')
@click.argument('args', nargs=-1, metavar="auditType=auditType source=source status=status createdBy=createdBy tableName=tableName tableRecordName=tableRecordName updatedTimeType=updatedTimeType updatedTime=updatedTime tableKey=tableKey includeChildAudits=includeChildAudits")
@click.pass_obj
@output_option
@select_option
def list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.audits.list_audit(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('get', short_help='Retrieves information on a specific Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agentclusterid=value agentclustername=value')
@click.pass_obj
@output_option
@select_option
def get_agent_cluster(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.get_agent_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('update', short_help='Modifies the Agent Cluster specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value opswise_groups=value strict_bsrvc_membership=value distribution=value network_alias=value network_alias_port=value resolution_status=value resolution_description=value last_resolution=value limit_type=value limit_amount=value current_count=value suspended=value suspended_on=value resumed_on=value agent_limit_type=value agent_limit_amount=value last_agent_used=value ignore_inactive_agents=value ignore_suspended_agents=value retain_sys_ids=value agents=value notifications=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_agent_cluster(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.agent_clusters.update_agent_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('create', short_help='Creates a new Agent Cluster.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_agent_cluster(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.agent_clusters.create_agent_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('delete', short_help='Deletes a specific Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agentclusterid=value agentclustername=value')
@click.pass_obj
@output_option
@select_option
def delete_agent_cluster(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.delete_agent_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('list', short_help='Retrieves information on all Agent Clusters.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_agent_clusters(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.list_agent_clusters(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('list_advanced', short_help='Retrieves Agent Cluster details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='agentclustername=value type=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_agent_clusters_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.list_agent_clusters_advanced(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('get_selected_agent', short_help='Retrieves information on a specific Agent from an Agent Cluster for which a Distribution method of Any or Lowest CPU Utilization is specified.')
@click.argument('args', nargs=-1, metavar='agentclustername=value ignoreexecutionlimit=value')
@click.pass_obj
@output_option
@select_option
def get_selected_agent(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.get_selected_agent(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('resolve_cluster', short_help='Resolves the Network Alias for the specified Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agent_cluster_name=value')
@click.pass_obj
@output_option
@select_option
def resolve_cluster(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.resolve_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('resume', short_help='Resumes the specified Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agent_cluster_name=value')
@click.pass_obj
@output_option
@select_option
def resume_cluster(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.resume_cluster(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('set_task_execution_limit', short_help='Sets the task execution limit for the specified Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agent_cluster_name=value limit_type=value limit_amount=value')
@click.pass_obj
@output_option
@select_option
def set_cluster_task_execution_limit(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.set_cluster_task_execution_limit(**vars_dict)
    process_output(output, select, response)


@agent_cluster.command('suspend', short_help='Suspends the specified Agent Cluster.')
@click.argument('args', nargs=-1, metavar='agent_cluster_name=value')
@click.pass_obj
@output_option
@select_option
def suspend_cluster(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agent_clusters.suspend_cluster(**vars_dict)
    process_output(output, select, response)


@agent.command('get', short_help='Retrieves information on a specific Agent.')
@click.argument('args', nargs=-1, metavar='agentid=value agentname=value')
@click.pass_obj
@output_option
@select_option
def get_agent(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.get_agent(**vars_dict)
    process_output(output, select, response)


@agent.command('update', short_help='Modifies the Agent specified by the sysId.')
@click.argument('args', nargs=-1, metavar='name=value description=value host_name=value queue_name=value ip_address=value log_level=value version=value build=value build_date=value ext_api_level_min=value ext_api_level_max=value extensions=value ext_accept=value ext_accept_list=value hb_intvl=value hb_grace_period=value cpu_load=value os=value os_release=value cpu=value hb_date=value start_date=value status=value jobs=value credentials=value pid=value limit_type=value limit_amount=value current_count=value suspended=value decommissioned=value decommissioned_date=value output_prohibited=value oms_server=value sys_id=value auth_version=value opswise_groups=value exclude_related=value credentials_required=value notifications=value transient=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_agent(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.agents.update_agent(**vars_dict)
    process_output(output, select, response)


@agent.command('delete', short_help='Deletes an Agent.')
@click.argument('args', nargs=-1, metavar='agentid=value agentname=value')
@click.pass_obj
@output_option
@select_option
def delete_agent(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.delete_agent(**vars_dict)
    process_output(output, select, response)


@agent.command('list', short_help='Retrieves information on all agents.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_agents(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.list_agents(**vars_dict)
    process_output(output, select, response)


@agent.command('list_advanced', short_help='Retrieves Agent details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='agentname=value type=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_agents_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.list_agents_advanced(**vars_dict)
    process_output(output, select, response)


@agent.command('resume', short_help='Resumes the specified agent.')
@click.argument('args', nargs=-1, metavar='agent_name=value agent_i_d=value')
@click.pass_obj
@output_option
@select_option
def resume_agent(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.resume_agent(**vars_dict)
    process_output(output, select, response)


@agent.command('resume_membership', short_help='Resumes the specified agent cluster membership.')
@click.argument('args', nargs=-1, metavar='agent_name=value agent_cluster_name=value agent_i_d=value')
@click.pass_obj
@output_option
@select_option
def resume_agent_cluster_membership(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.resume_agent_cluster_membership(**vars_dict)
    process_output(output, select, response)


@agent.command('set_task_execution_limit', short_help='Sets the task execution limit for the specified agent.')
@click.argument('args', nargs=-1, metavar='agent_name=value agent_i_d=value limit_type=value limit_amount=value')
@click.pass_obj
@output_option
@select_option
def set_agent_task_execution_limit(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.set_agent_task_execution_limit(**vars_dict)
    process_output(output, select, response)


@agent.command('suspend', short_help='Suspends the specified agent.')
@click.argument('args', nargs=-1, metavar='agent_name=value agent_i_d=value')
@click.pass_obj
@output_option
@select_option
def suspend_agent(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.suspend_agent(**vars_dict)
    process_output(output, select, response)


@agent.command('suspend_membership', short_help='Suspends the specified agent cluster membership.')
@click.argument('args', nargs=-1, metavar='agent_name=value agent_cluster_name=value agent_i_d=value')
@click.pass_obj
@output_option
@select_option
def suspend_agent_cluster_membership(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.agents.suspend_agent_cluster_membership(**vars_dict)
    process_output(output, select, response)


@audit.command('list', short_help='Retrieve the audit details using a specific filter.')
@click.argument('args', nargs=-1, metavar='audit_type=value source=value status=value created_by=value table_name=value table_record_name=value updated_time_type=value updated_time=value table_key=value include_child_audits=value')
@click.pass_obj
@output_option
@select_option
def list_audit(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.audits.list_audit(**vars_dict)
    process_output(output, select, response)


@bundle.command('promote', short_help='Promote a Bundle or schedule the promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='id=value name=value promotion_target_id=value promotion_target_name=value notification_option=value override_user=value override_password=value date=value time=value schedule=value create_snapshot=value allow_unv_tmplt_changes=value override_token=value')
@click.pass_obj
@output_option
@select_option
def promote(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.promote(**vars_dict)
    process_output(output, select, response)


@bundle.command('get', short_help='Retrieve Bundle details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def get_bundle(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('update', short_help='Modifies the Bundle specified by the sysId.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value name=value sys_id=value description=value opswise_groups=value default_promotion_target=value exclude_on_existence=value follow_references=value promote_bundle_definition=value promote_by_business_services=value visible_to=value bundle_agent_clusters=value bundle_applications=value bundle_business_services=value bundle_calendars=value bundle_credentials=value bundle_custom_days=value bundle_database_connections=value bundle_email_connections=value bundle_email_templates=value bundle_o_auth_clients=value bundle_peoplesoft_connections=value bundle_reports=value bundle_sap_connections=value bundle_scripts=value bundle_snmp_managers=value bundle_tasks=value bundle_triggers=value bundle_universal_event_templates=value bundle_universal_templates=value bundle_variables=value bundle_virtual_resources=value version=value exclude_related=value export_release_level=value export_table=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_bundle(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.bundles.update_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('create', short_help='Creates a Bundle.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_bundle(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('delete', short_help='Deletes the specified Bundle.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def delete_bundle(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('create_by_date', short_help='Creates a Bundle by Date.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_bundle_by_date(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_bundle_by_date(**vars_dict)
    process_output(output, select, response)


@bundle.command('get_report', short_help='Retrieve Bundle Report details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def get_bundle_report(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_bundle_report(**vars_dict)
    process_output(output, select, response)


@bundle.command('list', short_help='Retrieves information on all Bundles.')
@click.argument('args', nargs=-1, metavar='bundlename=value business_services=value default_promotion_target=value')
@click.pass_obj
@output_option
@select_option
def list_bundles(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.list_bundles(**vars_dict)
    process_output(output, select, response)


@business_service.command('get', short_help='Retrieves information on a specific Business Service.')
@click.argument('args', nargs=-1, metavar='busserviceid=value busservicename=value')
@click.pass_obj
@output_option
@select_option
def get_business_service(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.business_services.get_business_service(**vars_dict)
    process_output(output, select, response)


@business_service.command('update', short_help='Modifies the Business Service specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_business_service(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.business_services.update_business_service(**vars_dict)
    process_output(output, select, response)


@business_service.command('create', short_help='Creates a Business Service.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_business_service(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.business_services.create_business_service(**vars_dict)
    process_output(output, select, response)


@business_service.command('delete', short_help='Deletes a Business Service.')
@click.argument('args', nargs=-1, metavar='busserviceid=value busservicename=value')
@click.pass_obj
@output_option
@select_option
def delete_business_service(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.business_services.delete_business_service(**vars_dict)
    process_output(output, select, response)


@business_service.command('list', short_help='Retrieves information on all Business Services.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_business_services(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.business_services.list_business_services(**vars_dict)
    process_output(output, select, response)


@calendar.command('get', short_help='Retrieves information on all Custom Days of a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def get_custom_days(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.get_custom_days(**vars_dict)
    process_output(output, select, response)


@calendar.command('add', short_help='Adds the specified Custom Day to the specified Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def add_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.add_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('remove', short_help='Removes the specified Custom Day from a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def remove_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.remove_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('get', short_help='Retrieves information on a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def get_calendar(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.get_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('update', short_help='Modifies the Calendar specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value comments=value opswise_groups=value business_days=value first_quarter_start=value second_quarter_start=value third_quarter_start=value fourth_quarter_start=value retain_sys_ids=value first_day_of_week=value custom_days=value local_custom_days=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_calendar(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.calendars.update_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('create', short_help='Creates a new Calendar.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_calendar(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.calendars.create_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('delete', short_help='Deletes the specified Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def delete_calendar(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.delete_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('list', short_help='Retrieves information on all Calendars.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_calendars(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_calendars(**vars_dict)
    process_output(output, select, response)


@calendar.command('list_qualifying_dates_for_local_custom_day', short_help='Retrieves information on Qualifying Dates for a specific Local Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayname=value calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_dates_for_local_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_qualifying_dates_for_local_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('list_qualifying_periods', short_help='Retrieves information on Qualifying Periods for a specific Local Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayname=value calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_periods(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_qualifying_periods(**vars_dict)
    process_output(output, select, response)


@cluster_node.command('get', short_help='Retrieves information on the current Cluster Node.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def get_cluster_node(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.cluster_nodes.get_cluster_node(**vars_dict)
    process_output(output, select, response)


@cluster_node.command('list', short_help='Retrieves information on all Cluster Nodes.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_cluster_nodes(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.cluster_nodes.list_cluster_nodes(**vars_dict)
    process_output(output, select, response)


@credential.command('change_password', short_help='Changes the runtime password of the Credential based on name.')
@click.argument('args', nargs=-1, metavar='name=value new_runtime_password=value')
@click.pass_obj
@output_option
@select_option
def change_password(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.credentials.change_password(**vars_dict)
    process_output(output, select, response)


@credential.command('get', short_help='Retrieves information on a specific Credential.')
@click.argument('args', nargs=-1, metavar='credentialid=value credentialname=value')
@click.pass_obj
@output_option
@select_option
def get_credential(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    uac.log.debug('vars_dict: %s', vars_dict)
    response = uac.credentials.get_credential(**vars_dict)
    process_output(output, select, response)


@credential.command('update', short_help='Modifies the Credential specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value retain_sys_ids=value runtime_user=value runtime_password=value runtime_pass_phrase=value runtime_token=value provider=value provider_parameters=value runtime_key_location=value type=value opswise_groups=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_credential(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.credentials.update_credential(**vars_dict)
    process_output(output, select, response)


@credential.command('create', short_help='Creates a Credential.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_credential(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.credentials.create_credential(**vars_dict)
    process_output(output, select, response)


@credential.command('delete', short_help='Deletes the specified Credential.')
@click.argument('args', nargs=-1, metavar='credentialid=value credentialname=value')
@click.pass_obj
@output_option
@select_option
def delete_credential(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.credentials.delete_credential(**vars_dict)
    process_output(output, select, response)


@credential.command('list', short_help='Retrieves information on all Credentials.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_credentials(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.credentials.list_credentials(**vars_dict)
    process_output(output, select, response)


@credential.command('test_provider', short_help='None')
@click.argument('args', nargs=-1, metavar='credentialid=value credentialname=value')
@click.pass_obj
@output_option
@select_option
def test_provider(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    uac.log.debug('vars_dict: %s', vars_dict)
    response = uac.credentials.test_provider(**vars_dict)
    process_output(output, select, response)


@custom_day.command('get', short_help='Retrieves information on a specific Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def get_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.custom_days.get_custom_day(**vars_dict)
    process_output(output, select, response)


@custom_day.command('update', short_help='Modifies the Custom Day specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value comments=value category=value ctype=value month=value dayofweek=value relfreq=value day=value date=value date_list=value adjustment=value adjustment_amount=value adjustment_type=value nth_amount=value nth_type=value retain_sys_ids=value observed_rules=value period=value holiday=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_custom_day(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.custom_days.update_custom_day(**vars_dict)
    process_output(output, select, response)


@custom_day.command('create', short_help='Creates a new Custom Day.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_custom_day(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.custom_days.create_custom_day(**vars_dict)
    process_output(output, select, response)


@custom_day.command('delete', short_help='Deletes a specific Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def delete_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.custom_days.delete_custom_day(**vars_dict)
    process_output(output, select, response)


@custom_day.command('list', short_help='Retrieves information on all Custom Days.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_custom_days(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.custom_days.list_custom_days(**vars_dict)
    process_output(output, select, response)


@custom_day.command('list_qualifying_dates', short_help='Retrieves information on Qualifying Dates for a specific Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayid=value customdayname=value calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_dates(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.custom_days.list_qualifying_dates(**vars_dict)
    process_output(output, select, response)


@database.command('get', short_help='Retrieves information on a specific Database Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_database_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.get_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('update', short_help='Modifies the Database Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value db_type=value db_url=value db_driver=value db_max_rows=value db_description=value credentials=value retain_sys_ids=value opswise_groups=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_database_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.databaseconnections.update_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('create', short_help='Creates a Database Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_database_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.databaseconnections.create_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('delete', short_help='Deletes the specified Database Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_database_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.delete_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('list', short_help='Retrieves information on all Database Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_database_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.list_database_connections(**vars_dict)
    process_output(output, select, response)


@email.command('get', short_help='Retrieves information on a specific Email Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_email_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.get_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('update', short_help='Modifies the Email Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value smtp=value smtp_port=value smtp_ssl=value smtp_starttls=value email_addr=value default_user=value default_pwd=value authentication=value authentication_type=value oauth_client=value system_connection=value type=value imap=value imap_port=value imap_ssl=value imap_starttls=value trash_folder=value opswise_groups=value description=value authorized=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_email_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.emailconnections.update_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('create', short_help='Creates an Email Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_email_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.emailconnections.create_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('delete', short_help='Deletes the specified Email Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_email_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.delete_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('list', short_help='Retrieves information on all Email Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_email_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.list_email_connections(**vars_dict)
    process_output(output, select, response)


@email_template.command('get', short_help='Retrieves information on a specific Email Template.')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_email_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.email_templates.get_email_template(**vars_dict)
    process_output(output, select, response)


@email_template.command('update', short_help='Modifies the Email Template specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value template_name=value description=value opswise_groups=value connection=value reply_to=value to=value cc=value bcc=value subject=value body=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_email_template(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.email_templates.update_email_template(**vars_dict)
    process_output(output, select, response)


@email_template.command('create', short_help='Creates an Email Template.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_email_template(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.email_templates.create_email_template(**vars_dict)
    process_output(output, select, response)


@email_template.command('delete', short_help='Deletes the specified Email Template.')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_email_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.email_templates.delete_email_template(**vars_dict)
    process_output(output, select, response)


@email_template.command('list', short_help='Retrieves information on all Email Templates..')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_email_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.email_templates.list_email_template(**vars_dict)
    process_output(output, select, response)


@ldap.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def get_ldap(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.ldap.get_ldap(**vars_dict)
    process_output(output, select, response)


@ldap.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value url=value bind_dn=value bind_password=value use_for_authentication=value allow_local_login=value base_dn=value user_id_attribute=value user_filter=value group_filter=value connect_timeout=value read_timeout=value user_membership_attribute=value group_member_attribute=value login_method=value user_target_ou_list=value group_target_ou_list=value mappings=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_ldap(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.ldap.update_ldap(**vars_dict)
    process_output(output, select, response)


@metrics.command('get', short_help='Scrapes the Universal Controller metrics as Prometheus text.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
def get_metrics(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.metrics.get_metrics(**vars_dict)
    process_output(output, select, response, text=True)


@oauth_client.command('get', short_help='Retrieves information on a specific OAuth Client')
@click.argument('args', nargs=-1, metavar='oauthclientid=value oauthclientname=value')
@click.pass_obj
@output_option
@select_option
def get_o_auth_client(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oauth_clients.get_o_auth_client(**vars_dict)
    process_output(output, select, response)


@oauth_client.command('update', short_help='Modifies the OAuth Client specified by the sysId..')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value opswise_groups=value provider=value cluster_redirect_urls=value authorization_endpoint=value token_endpoint=value tenant_id=value client_id=value client_secret=value scopes=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_o_auth_client(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.oauth_clients.update_o_auth_client(**vars_dict)
    process_output(output, select, response)


@oauth_client.command('create', short_help='Creates an OAuth Client.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_o_auth_client(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.oauth_clients.create_o_auth_client(**vars_dict)
    process_output(output, select, response)


@oauth_client.command('delete', short_help='Deletes the specified OAuth Client.')
@click.argument('args', nargs=-1, metavar='oauthclientid=value oauthclientname=value')
@click.pass_obj
@output_option
@select_option
def delete_o_auth_client(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oauth_clients.delete_o_auth_client(**vars_dict)
    process_output(output, select, response)


@oauth_client.command('list', short_help='Retrieves information on all OAuth Clients.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_o_auth_clients(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oauth_clients.list_o_auth_clients(**vars_dict)
    process_output(output, select, response)


@oms_server.command('get', short_help='Retrieves information on a specific OMS Server.')
@click.argument('args', nargs=-1, metavar='serveraddress=value serverid=value')
@click.pass_obj
@output_option
@select_option
def get_oms_server(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oms_servers.get_oms_server(**vars_dict)
    process_output(output, select, response)


@oms_server.command('update', short_help='Modifies the OMS Server specified by the sysId. To modify OMS Server properties without modifying related records, set excludeRelated = true.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value server_address=value description=value opswise_groups=value status=value timeout=value session_status=value suspended=value last_connected=value last_connected_time=value authenticate=value retain_sys_ids=value notifications=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_oms_server(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.oms_servers.update_oms_server(**vars_dict)
    process_output(output, select, response)


@oms_server.command('create', short_help='Creates an OMS Server.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_oms_server(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.oms_servers.create_oms_server(**vars_dict)
    process_output(output, select, response)


@oms_server.command('delete', short_help='Deletes the specified OMS Server.')
@click.argument('args', nargs=-1, metavar='serveraddress=value serverid=value')
@click.pass_obj
@output_option
@select_option
def delete_oms_server(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oms_servers.delete_oms_server(**vars_dict)
    process_output(output, select, response)


@oms_server.command('list', short_help='Retrieves the Server address or partial server address of all OMS servers.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_oms_servers(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.oms_servers.list_oms_servers(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('get', short_help='Retrieves information on a specific PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_peoplesoft_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.get_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('update', short_help='Modifies the PeopleSoft Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value server=value port=value endpoint=value credentials=value retain_sys_ids=value opswise_groups=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_peoplesoft_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.peoplesoftconnections.update_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('create', short_help='Creates a PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_peoplesoft_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.peoplesoftconnections.create_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('delete', short_help='Deletes the specified PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_peoplesoft_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.delete_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('list', short_help='Retrieves information on all PeopleSoft Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_peoplesoft_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.list_peoplesoft_connections(**vars_dict)
    process_output(output, select, response)


# @promote.command('promote_1', short_help='Promotes, without a bundle, one or more items of a specific type.')
# @click.argument('args', nargs=-1, metavar='item_type=value item_ids=value item_names=value items=value promotion_target_id=value promotion_target_name=value override_user=value override_password=value exclude_on_existence=value follow_references=value allow_unv_tmplt_changes=value override_token=value')
# @click.pass_obj
# @output_option
# @select_option
# def promote_1(uac, args, output=None, select=None):
#     vars_dict = process_input(args)
#     response = uac.promotes.promote_1(**vars_dict)
#     process_output(output, select, response)


@promotion.command('cancel_promotion_schedule', short_help='Cancels the scheduled promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='scheduleid=value bundleid=value bundlename=value date=value time=value')
@click.pass_obj
@output_option
@select_option
def cancel_promotion_schedule(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.cancel_promotion_schedule(**vars_dict)
    process_output(output, select, response)


@promotion.command('delete', short_help='Deletes the scheduled promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='scheduleid=value bundleid=value bundlename=value date=value time=value')
@click.pass_obj
@output_option
@select_option
def delete_promotion_schedule(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_promotion_schedule(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('get', short_help='Retrieve a specified Promotion Target details.')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value')
@click.pass_obj
@output_option
@select_option
def get_promotion_target(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('update', short_help='Modifies the specified Promotion Target.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value name=value description=value uri=value user=value password=value authentication_method=value opswise_groups=value token=value agent_mappings=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_promotion_target(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.bundles.update_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('create', short_help='Creates a Promotion Target.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_promotion_target(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('delete', short_help='Deletes the specified Promotion Target.')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value')
@click.pass_obj
@output_option
@select_option
def delete_promotion_target(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('list', short_help='Retrieves information on all Promotion Targets.')
@click.argument('args', nargs=-1, metavar='targetname=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_promotion_targets(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.list_promotion_targets(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('refresh_target_agents', short_help='None')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value username=value password=value token=value')
@click.pass_obj
@output_option
@select_option
def refresh_target_agents(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.refresh_target_agents(**vars_dict)
    process_output(output, select, response)


@property.command('get', short_help='Retrieves information on a specific property.')
@click.argument('args', nargs=-1, metavar='propertyname=value')
@click.pass_obj
@output_option
@select_option
def get_property(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.properties.get_property(**vars_dict)
    process_output(output, select, response)


@property.command('update', short_help='Modifies the specified property.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@input_option
@select_option
def update_property(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.properties.update_property(**vars_dict)
    process_output(output, select, response)


@property.command('list', short_help='Retrieves information on all properties.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_properties(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.properties.list_properties(**vars_dict)
    process_output(output, select, response)


@report.command('run_report', short_help='None')
@click.argument('args', nargs=-1, metavar='reporttitle=value visibility=value groupname=value format=')
@click.pass_obj
@output_option_binary
@select_option
@click.option("--format", type=click.Choice(["csv", "tab", "pdf", "png", "xml", "json"]))
def run_report(uac, args, output=None, select=None, format="csv"):
    vars_dict = process_input(args)
    response = uac.reports.run_report(report_format=format, **vars_dict)
    process_output(output, select, response, text=True, binary=(format in ["pdf", "png"]))


@sap.command('get', short_help='Retrieves information on a specific SAP Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_sap_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.get_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('update', short_help='Modifies the SAP Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value sap_connection_type=value sap_ashost=value sap_client=value sap_sysnr=value sap_gwhost=value sap_gwserv=value sap_r3name=value sap_mshost=value sap_group=value opswise_groups=value description=value sap_saprouter=value sap_snc_mode=value sap_snc_lib=value sap_snc_myname=value sap_snc_partnername=value sap_snc_qop=value sap_snc_sso=value sap_mysapsso2=value sap_x509cert=value sap_use_symbolic_names=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_sap_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.sapconnections.update_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('create', short_help='Creates an SAP Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_sap_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.sapconnections.create_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('delete', short_help='Deletes the specified SAP Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_sap_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.delete_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('list', short_help='Retrieves information on all SAP Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_sap_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.list_sap_connections(**vars_dict)
    process_output(output, select, response)


@script.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='scriptid=value scriptname=value')
@click.pass_obj
@output_option
@select_option
def get_script(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.scripts.get_script(**vars_dict)
    process_output(output, select, response)


@script.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value script_name=value script_type=value description=value content=value resolve_variables=value retain_sys_ids=value opswise_groups=value notes=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_script(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.scripts.update_script(**vars_dict)
    process_output(output, select, response)


@script.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_script(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.scripts.create_script(**vars_dict)
    process_output(output, select, response)


@script.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='scriptid=value scriptname=value')
@click.pass_obj
@output_option
@select_option
def delete_script(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.scripts.delete_script(**vars_dict)
    process_output(output, select, response)


@script.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_scripts(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.scripts.list_scripts(**vars_dict)
    process_output(output, select, response)


@server_operation.command('roll_log', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def roll_log(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.serveroperations.roll_log(**vars_dict)
    process_output(output, select, response)


@server_operation.command('temporary_property_change', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value value=value')
@click.pass_obj
@output_option
@select_option
def temporary_property_change(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.serveroperations.temporary_property_change(**vars_dict)
    process_output(output, select, response)


@simulation.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='simulationid=value taskname=value workflowname=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def get_simulation(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.simulations.get_simulation(**vars_dict)
    process_output(output, select, response)


@simulation.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value task=value workflow=value vertex_id=value status=value exit_code=value publish_status=value publish_late_start=value publish_late_finish=value publish_early_finish=value abort_actions=value email_notification_actions=value variable_actions=value snmp_notification_actions=value system_operation_actions=value other_options=value outputs=value variables_from_string=value variables=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_simulation(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.simulations.update_simulation(**vars_dict)
    process_output(output, select, response)


@simulation.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_simulation(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.simulations.create_simulation(**vars_dict)
    process_output(output, select, response)


@simulation.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='simulationid=value taskname=value workflowname=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def delete_simulation(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.simulations.delete_simulation(**vars_dict)
    process_output(output, select, response)


@simulation.command('list_simulations', short_help='None')
@click.argument('args', nargs=-1, metavar='taskname=value workflowname=value')
@click.pass_obj
@output_option
@select_option
def list_simulations(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.simulations.list_simulations(**vars_dict)
    process_output(output, select, response)


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


@system.command('get', short_help='None')
@click.pass_obj
@output_option
@select_option
def get_status(uac, output=None, select=None):
    response = uac.system.get_status()
    process_output(output, select, response)


@task_instance.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def delete_task_instance(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.delete_task_instance(**vars_dict)
    process_output(output, select, response)


@task_instance.command('show_variables', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value fetchglobal=value')
@click.pass_obj
@output_option
@select_option
def show_variables(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.show_variables(**vars_dict)
    process_output(output, select, response)


@task_instance.command('update_operational_memo', short_help='None')
@click.argument('args', nargs=-1, metavar='memo=message taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_operational_memo(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.task_instances.update_operational_memo(**vars_dict)
    process_output(output, select, response)


@task_instance.command('set_priority', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_set_priority(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_priority(**vars_dict)
    process_output(output, select, response)

@task_instance.command('set_complete', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value operationalMemo=value')
@click.pass_obj
@output_option
@select_option
def task_instance_set_priority(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_complete(**vars_dict)
    process_output(output, select, response)


@task_instance.command('set_timewait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def set_timewait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_timewait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('list_dependency_list', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value dependencytype=value')
@click.pass_obj
@output_option
@select_option
def list_dependency_list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.list_dependency_list(**vars_dict)
    process_output(output, select, response)


@task_instance.command('task_insert', short_help='None')
@click.argument('args', nargs=-1, metavar='id=value name=value alias=value workflow_instance_id=value workflow_instance_name=value workflow_instance_criteria=value predecessors=value successors=value vertex_x=value vertex_y=value inherit_trigger_time=value')
@click.pass_obj
@output_option
@select_option
def task_insert(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    if "predecessors" in vars_dict:
        vars_dict["predecessors"] = vars_dict["predecessors"].split(",")
    if "successors" in vars_dict:
        vars_dict["successors"] = vars_dict["successors"].split(",")
    response = uac.task_instances.task_insert(**vars_dict)
    process_output(output, select, response)


@task_instance.command('cancel', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_cancel(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.cancel(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_dependencies', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_dependencies(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_dependencies(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_exclusive', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_exclusive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_exclusive(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_instance_wait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_instance_wait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_instance_wait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_predecessors', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_predecessors(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_predecessors(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_resources', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_resources(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_resources(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_timewait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_timewait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_timewait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('force_finish', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_force_finish(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.force_finish(**vars_dict)
    process_output(output, select, response)


@task_instance.command('force_finish_cancel', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_force_finish_cancel(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.force_finish_cancel(**vars_dict)
    process_output(output, select, response)


@task_instance.command('hold', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_hold(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.hold(**vars_dict)
    process_output(output, select, response)


@task_instance.command('release', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_release(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.release(**vars_dict)
    process_output(output, select, response)


@task_instance.command('rerun', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_rerun(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.rerun(**vars_dict)
    process_output(output, select, response)


@task_instance.command('retrieve_output', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value outputtype=value startline=value numlines=value scantext=value operational_memo=value')
@click.pass_obj
@output_option
@select_option
def task_instance_retrieve_output(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.retrieve_output(**vars_dict)
    process_output(output, select, response)


@task_instance.command('skip', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_skip(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.skip(**vars_dict)
    process_output(output, select, response)


@task_instance.command('skip_path', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_skip_path(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.skip_path(**vars_dict)
    process_output(output, select, response)


@task_instance.command('unskip', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value')
@click.pass_obj
@output_option
@select_option
def task_instance_unskip(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.unskip(**vars_dict)
    process_output(output, select, response)


@task_instance.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value agent_name=value workflow_instance_criteria=value workflow_instance_id=value status=value type=value execution_user=value late_start=value late_finish=value early_finish=value started_late=value finished_late=value finished_early=value late=value late_early=value business_services=value updated_time_type=value updated_time=value sys_id=value instance_number=value task_id=value task_name=value custom_field1=value custom_field2=value trigger_id=value trigger_name=value workflow_definition_id=value workflow_definition_name=value status_description=value template_id=value template_name=value response_fields=value instance_output_type=value')
@click.pass_obj
@output_option
@select_option
def list_status(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.list_status(**vars_dict)
    process_output(output, select, response)


@task.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='taskid=value taskname=value')
@click.pass_obj
@output_option
@select_option
def get_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.get_task(**vars_dict)
    process_output(output, select, response)


@task.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value variables=value notes=value actions=value retain_sys_ids=value name=value resolve_name_immediately=value summary=value opswise_groups=value start_held=value start_held_reason=value res_priority=value hold_resources=value credentials=value credentials_var=value credentials_var_check=value retry_maximum=value retry_indefinitely=value retry_interval=value retry_suppress_failure=value ls_enabled=value ls_type=value ls_time=value ls_day_constraint=value ls_nth_amount=value ls_duration=value lf_enabled=value lf_type=value lf_time=value lf_day_constraint=value lf_nth_amount=value lf_duration=value lf_offset_type=value lf_offset_percentage=value lf_offset_duration=value lf_offset_duration_unit=value ef_enabled=value ef_type=value ef_time=value ef_day_constraint=value ef_nth_amount=value ef_duration=value ef_offset_type=value ef_offset_percentage=value ef_offset_duration=value ef_offset_duration_unit=value user_estimated_duration=value cp_duration=value cp_duration_unit=value tw_wait_type=value tw_wait_amount=value tw_wait_time=value tw_wait_duration=value tw_wait_day_constraint=value tw_delay_type=value tw_delay_amount=value tw_delay_duration=value tw_workflow_only=value custom_field1=value custom_field2=value execution_restriction=value restriction_period=value restriction_period_before_date=value restriction_period_after_date=value restriction_period_before_time=value restriction_period_after_time=value restriction_period_date_list=value log_level=value exclusive_with_self=value min_run_time=value max_run_time=value avg_run_time=value last_run_time=value min_run_time_display=value max_run_time_display=value avg_run_time_display=value last_run_time_display=value run_count=value run_time=value first_run=value last_run=value simulation=value enforce_variables=value lock_variables=value override_instance_wait=value time_zone_pref=value virtual_resources=value exclusive_tasks=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_task(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.tasks.update_task(**vars_dict)
    process_output(output, select, response)


@task.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_task(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.tasks.create_task(**vars_dict)
    process_output(output, select, response)


@task.group(name='new', short_help='Create new tasks from template.')
def new_task():
    pass


@new_task.command('linux', short_help='Create new Linux tasks from template.')
@click.argument('args', nargs=-1, metavar='name=taskname agent=agent_name command=[command to execute] script=[name of the script to execute]' )
@click.pass_obj
@output_option
@select_option
def linux_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_linux_task(**vars_dict)
    process_output(output, select, response)

@new_task.command('windows', short_help='Create new Windows tasks from template.')
@click.argument('args', nargs=-1, metavar='name=taskname agent=agent_name command=[command to execute] script=[name of the script to execute]' )
@click.pass_obj
@output_option
@select_option
def linux_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_windows_task(**vars_dict)
    process_output(output, select, response)

@new_task.command('workflow', short_help='Create new Workflow tasks from template.')
@click.argument('args', nargs=-1, metavar='name=[workflow name]' )
@click.pass_obj
@output_option
@select_option
def workflow_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_workflow(**vars_dict)
    process_output(output, select, response)

@task.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='taskid=value taskname=value')
@click.pass_obj
@output_option
@select_option
def delete_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.delete_task(**vars_dict)
    process_output(output, select, response)


@task.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value enabled=value type=value business_services=value updated_time_type=value updated_time=value workflow_id=value workflow_name=value agent_name=value description=value tasks=value template_id=value template_name=value')
@click.pass_obj
@output_option
@select_option
def list_tasks(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_tasks(**vars_dict)
    process_output(output, select, response)


@task.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='taskname=value agentname=value type=value business_services=value workflowname=value workflowid=value updated_time=value updated_time_type=value templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def list_tasks_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_tasks_advanced(**vars_dict)
    process_output(output, select, response)


@task.command('list_workflow_list', short_help='None')
@click.argument('args', nargs=-1, metavar='taskname=value taskid=value')
@click.pass_obj
@output_option
@select_option
def list_workflow_list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_workflow_list(**vars_dict)
    process_output(output, select, response)


@task.command('list_dependency_list_1', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value dependencytype=value')
@click.pass_obj
@output_option
@select_option
def list_dependency_list_1(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_dependency_list_1(**vars_dict)
    process_output(output, select, response)


@task.command('launch', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value hold=value hold_reason=value time_zone=value virtual_resource_priority=value virtual_resources=value launch_reason=value simulate=value variables=value variables_map=value')
@click.pass_obj
@output_option
@select_option
@click.option('--wait', '-w', is_flag=True)
@click.option('--timeout', '-t', type=int, default=300)
@click.option('--interval', '-i', type=int, default=10)
@click.option('--return_rc', '-r', is_flag=True)
def task_launch(uac, args, output=None, select=None, wait=False, timeout=300, interval=10, return_rc=False):
    vars_dict = process_input(args)
    if wait:
        response = uac.tasks.task_launch_and_wait(timeout=timeout, interval=interval, **vars_dict)
    else:
        response = uac.tasks.task_launch(**vars_dict)
    process_output(output, select, response)
    if wait and return_rc:
        if "exitCode" in response:
            exit(int(response["exitCode"]))
        else:
            if response.get("status", "UNKNOWN") in uac.task_instances.SUCCESS_STATUSES:
                exit(0)
            else:
                exit(1)





@trigger.command('list_qualifying_times', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value count=value startdate=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_times(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_qualifying_times(**vars_dict)
    process_output(output, select, response)


@trigger.command('unassign_execution_user', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def unassign_execution_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.unassign_execution_user(**vars_dict)
    process_output(output, select, response)

@trigger.command('assign_execution_user', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value username=username password=password')
@click.pass_obj
@output_option
@select_option
def unassign_execution_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.assign_execution_user_to_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_temp_trigger(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.triggers.create_temp_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def get_trigger(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.get_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value name=value description=value calendar=value enabled=value forecast=value restriction=value restriction_simple=value restriction_complex=value situation=value action=value restriction_mode=value restriction_adjective=value restriction_nth_amount=value restriction_noun=value restriction_nouns=value restriction_qualifier=value restriction_qualifiers=value skip_count=value skip_active=value simulation_option=value time_zone=value execution_user=value opswise_groups=value tasks=value retention_duration_purge=value retention_duration=value retention_duration_unit=value rd_exclude_backup=value skip_condition=value skip_restriction=value skip_after_date=value skip_after_time=value skip_before_date=value skip_before_time=value skip_date_list=value enabled_by=value enabled_time=value disabled_by=value disabled_time=value next_scheduled_time=value enforce_variables=value lock_variables=value custom_field1=value custom_field2=value variables=value notes=value restriction_qualifiers_from_string=value restriction_nouns_from_string=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_trigger(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.triggers.update_trigger(**vars_dict)
    process_output(output, select, response)

@trigger.command('enable_disable', short_help='None')
@click.argument('args', nargs=-1, metavar='enable=boolean name=triggername')
@click.pass_obj
@output_option
@input_option
@select_option
def enable_disable(uac, args, output=None, input=None, select=None):
    _payload = [create_payload(args)]
    response = uac.triggers.enable_disable(payload=_payload)
    process_output(output, select, response)


@trigger.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_trigger(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.triggers.create_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def delete_trigger(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.delete_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value enabled=value type=value business_services=value updated_time_type=value updated_time=value workflow_id=value workflow_name=value agent_name=value description=value tasks=value template_id=value template_name=value')
@click.pass_obj
@output_option
@select_option
def list_triggers(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_triggers(**vars_dict)
    process_output(output, select, response)


@trigger.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='triggername=value type=value business_services=value enabled=value tasks=value description=value')
@click.pass_obj
@output_option
@select_option
def list_triggers_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_triggers_advanced(**vars_dict)
    process_output(output, select, response)


@universal_event.command('publish', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value business_services=value ttl=value attributes=value')
@click.pass_obj
@output_option
@select_option
def publish(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.publish(**vars_dict)
    process_output(output, select, response)


@universal_event.command('pushg', short_help='None')
@click.argument('args', nargs=-1, metavar='payload=value')
@click.pass_obj
@output_option
@select_option
def pushg(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.pushg(**vars_dict)
    process_output(output, select, response)


@universal_event.command('push', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def push(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.push(**vars_dict)
    process_output(output, select, response)


@universal_event_template.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_universal_event_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_event_templates.get_universal_event_template(**vars_dict)
    process_output(output, select, response)


@universal_event_template.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value label=value description=value ttl=value attributes_policy=value attributes=value metric_type=value metric_name=value metric_value_attribute=value metric_unit=value metric_label_attributes=value metric_optional_labels=value retain_sys_ids=value attributes_from_string=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_universal_event_template(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.universal_event_templates.update_universal_event_template(**vars_dict)
    process_output(output, select, response)


@universal_event_template.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_universal_event_template(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.universal_event_templates.create_universal_event_template(**vars_dict)
    process_output(output, select, response)


@universal_event_template.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_universal_event_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_event_templates.delete_universal_event_template(**vars_dict)
    process_output(output, select, response)


@universal_event_template.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='templatename=value')
@click.pass_obj
@output_option
@select_option
def list_universal_event_templates(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_event_templates.list_universal_event_templates(**vars_dict)
    process_output(output, select, response)


@universal_template.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_universal_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.get_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value extension=value variable_prefix=value log_level=value icon_filename=value icon_filesize=value icon_date_created=value template_type=value agent_type=value use_common_script=value script=value script_unix=value script_windows=value script_type_windows=value always_cancel_on_finish=value send_variables=value credentials=value credentials_var=value credentials_var_check=value agent=value agent_var=value agent_var_check=value agent_cluster=value agent_cluster_var=value agent_cluster_var_check=value broadcast_cluster=value broadcast_cluster_var=value broadcast_cluster_var_check=value runtime_dir=value environment=value send_environment=value exit_codes=value exit_code_processing=value exit_code_text=value exit_code_output=value output_type=value output_content_type=value output_path_expression=value output_condition_operator=value output_condition_value=value output_condition_strategy=value auto_cleanup=value output_return_type=value output_return_file=value output_return_sline=value output_return_nline=value output_return_text=value wait_for_output=value output_failure_only=value elevate_user=value desktop_interact=value create_console=value agent_fields_restriction=value credential_fields_restriction=value environment_variables_fields_restriction=value exit_code_processing_fields_restriction=value automatic_output_retrieval_fields_restriction=value retain_sys_ids=value min_release_level=value environment_from_string=value fields=value commands=value events=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_universal_template(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.universal_templates.update_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_universal_template(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.universal_templates.create_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_universal_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.delete_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_extension_archive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.get_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('update_extension_archive', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@input_option
@select_option
def update_extension_archive(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.universal_templates.update_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('delete_extension_archive', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_extension_archive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.delete_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('export', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value exclude_extension=value')
@click.pass_obj
@output_option
@select_option
def export_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.export_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('set_icon', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def set_template_icon(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.set_template_icon(**vars_dict)
    process_output(output, select, response)


@universal_template.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='templatename=value')
@click.pass_obj
@output_option
@select_option
def list_universal_templates(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.list_universal_templates(**vars_dict)
    process_output(output, select, response)


@user_group.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='groupid=value groupname=value')
@click.pass_obj
@output_option
@select_option
def get_user_group(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.user_groups.get_user_group(**vars_dict)
    process_output(output, select, response)


@user_group.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value name=value email=value manager=value description=value parent=value ctrl_navigation_visibility=value navigation_visibility=value permissions=value group_roles=value group_members=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_user_group(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.user_groups.update_user_group(**vars_dict)
    process_output(output, select, response)


@user_group.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_user_group(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.user_groups.create_user_group(**vars_dict)
    process_output(output, select, response)


@user_group.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='groupid=value groupname=value')
@click.pass_obj
@output_option
@select_option
def delete_user_group(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.user_groups.delete_user_group(**vars_dict)
    process_output(output, select, response)


@user_group.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_user_groups(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.user_groups.list_user_groups(**vars_dict)
    process_output(output, select, response)


@user.command('change_password', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value new_password=value')
@click.pass_obj
@output_option
@select_option
def change_user_password(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.change_user_password(**vars_dict)
    process_output(output, select, response)


@user.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='userid=value username=value show_tokens=value')
@click.pass_obj
@output_option
@select_option
def get_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.get_user(**vars_dict)
    process_output(output, select, response)


@user.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value user_name=value user_password=value first_name=value middle_name=value last_name=value email=value title=value active=value locked_out=value password_needs_reset=value business_phone=value mobile_phone=value time_zone=value department=value manager=value browser_access=value command_line_access=value web_service_access=value login_method=value impersonate=value permissions=value user_roles=value tokens=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_user(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.users.update_user(**vars_dict)
    process_output(output, select, response)


@user.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='user_name="newuser" user_password="abc123"')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_user(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids, ignore_ids)
    uac.log.debug(vars_dict)
    uac.log.debug(args)
    vars_dict['payload']["userPassword"] = vars_dict.get('userPassword', vars_dict.get('user_password'))
    response = uac.users.create_user(**vars_dict)
    process_output(output, select, response)


@user.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='userid=value username=value')
@click.pass_obj
@output_option
@select_option
def delete_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.delete_user(**vars_dict)
    process_output(output, select, response)


@user.command('create_token', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value user_id=uuid user_name=userName name=token_name expiration=yyyy-mm-dd')
@click.pass_obj
@output_option
@input_option
@select_option
def create_user_token(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.users.create_user_token(**vars_dict)
    process_output(output, select, response)


@user.command('revoke_token', short_help='None')
@click.argument('args', nargs=-1, metavar='userid=value username=value tokenname=value')
@click.pass_obj
@output_option
@select_option
def revoke_user_token(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.revoke_user_token(**vars_dict)
    process_output(output, select, response)


@user.command('list_auth_tokens', short_help='None')
@click.argument('args', nargs=-1, metavar='userid=value username=value')
@click.pass_obj
@output_option
@select_option
def list_auth_tokens(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.list_auth_tokens(**vars_dict)
    process_output(output, select, response)


@user.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='show_tokens=value')
@click.pass_obj
@output_option
@select_option
def list_users(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.users.list_users(**vars_dict)
    process_output(output, select, response)


@variable.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='variableid=value variablename=value')
@click.pass_obj
@output_option
@select_option
def get_variable(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.variables.get_variable(**vars_dict)
    process_output(output, select, response)


@variable.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value value=value description=value opswise_groups=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_variable(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.variables.update_variable(**vars_dict)
    process_output(output, select, response)


@variable.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_variable(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.variables.create_variable(**vars_dict)
    process_output(output, select, response)


@variable.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='variableid=value variablename=value')
@click.pass_obj
@output_option
@select_option
def delete_variable(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.variables.delete_variable(**vars_dict)
    process_output(output, select, response)


@variable.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='variable_name=value scope=value task_name=value trigger_name=value')
@click.pass_obj
@output_option
@select_option
def list_variables(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.variables.list_variables(**vars_dict)
    process_output(output, select, response)


@variable.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='scope=value variablename=value taskname=value triggername=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_variables_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.variables.list_variables_advanced(**vars_dict)
    process_output(output, select, response)


@variable.command('set', short_help='None')
@click.argument('args', nargs=-1, metavar='scope=value create=value trigger=value task=value variable=value')
@click.pass_obj
@output_option
@input_option
@select_option
def variable_set(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.variables.variable_set(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='resourceid=value resourcename=value')
@click.pass_obj
@output_option
@select_option
def get_virtual_resource(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.virtual_resources.get_virtual_resource(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value limit=value summary=value type=value opswise_groups=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_virtual_resource(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.virtual_resources.update_virtual_resource(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_virtual_resource(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.virtual_resources.create_virtual_resource(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='resourceid=value resourcename=value')
@click.pass_obj
@output_option
@select_option
def delete_virtual_resource(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.virtual_resources.delete_virtual_resource(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value resourcename=value type=value')
@click.pass_obj
@output_option
@select_option
def list_virtual_resources(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.virtual_resources.list_virtual_resources(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='resourcename=value type=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_virtual_resources_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.virtual_resources.list_virtual_resources_advanced(**vars_dict)
    process_output(output, select, response)


@virtual_resource.command('update_limit', short_help='None')
@click.argument('args', nargs=-1, metavar='sys_id=value name=value limit=value description=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_limit(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.virtual_resources.update_limit(**vars_dict)
    process_output(output, select, response)


@webhook.command('unassign_execution_user_1', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookid=value webhookname=value')
@click.pass_obj
@output_option
@select_option
def unassign_execution_user_1(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.unassign_execution_user_1(**vars_dict)
    process_output(output, select, response)


@webhook.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookid=value webhookname=value')
@click.pass_obj
@output_option
@select_option
def get_webhook(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.get_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value retain_sys_ids=value opswise_groups=value event=value action=value task=value url=value filter=value enabled_by=value enabled_time=value disabled_by=value disabled_time=value execution_user=value status=value status_description=value url_parameters=value http_headers=value http_auth=value credentials=value url_parameters_from_string=value http_headers_from_string=value event_business_service_criteria=value event_business_services=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_webhook(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.webhooks.update_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_webhook(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.webhooks.create_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookid=value webhookname=value')
@click.pass_obj
@output_option
@select_option
def delete_webhook(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.delete_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('disable', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookid=value webhookname=value')
@click.pass_obj
@output_option
@select_option
def disable_webhook(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.disable_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('enable', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookid=value webhookname=value')
@click.pass_obj
@output_option
@select_option
def enable_webhook(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.enable_webhook(**vars_dict)
    process_output(output, select, response)


@webhook.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='webhookname=value action=value business_services=value description=value event=value task=value taskname=value url=value')
@click.pass_obj
@output_option
@select_option
def list_webhooks(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.webhooks.list_webhooks(**vars_dict)
    process_output(output, select, response)


@workflow.command('get_edges', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value sourceid=value targetid=value')
@click.pass_obj
@output_option
@select_option
def get_edges(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_edges(**vars_dict)
    process_output(output, select, response)


@workflow.command('update_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='sys_id=value workflow_id=value condition=value straight_edge=value points=value source_id=value target_id=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_edge(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.workflows.update_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('add_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value condition=value straight_edge=value points=value source_id=value target_id=value')
@click.pass_obj
@output_option
@select_option
def add_edge(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('delete_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value sourceid=value targetid=value')
@click.pass_obj
@output_option
@select_option
def delete_edge(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.delete_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('get_vertices', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value taskid=value taskname=value taskalias=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def get_vertices(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_vertices(**vars_dict)
    process_output(output, select, response)


@workflow.command('update_vertex', short_help='None')
@click.argument('args', nargs=-1, metavar='sys_id=value workflow_id=value task=value alias=value vertex_id=value vertex_x=value vertex_y=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_vertex(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.workflows.update_vertex(**vars_dict)
    process_output(output, select, response)


@workflow.command('add_vertex', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value task=value alias=value vertex_id=value vertex_x=value vertex_y=value')
@click.pass_obj
@output_option
@select_option
def add_vertex(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_vertex(**vars_dict)
    process_output(output, select, response)

@workflow.command('add_child_vertex', short_help='Adds a vertex and edge')
@click.argument('args', nargs=-1, metavar='workflow_name=value parent_task_name=name parent_vertex_id=[optional] task_name=new_task vertex_id=[optional] vertexX=None vertexY=None vertex_x_offset=100 vertex_y_offset=100')
@click.pass_obj
@output_option
@select_option
def add_child_vertex(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_child_vertex(**vars_dict)
    process_output(output, select, response)


@workflow.command('delete_vertices', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value taskid=value taskname=value taskalias=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def delete_vertices(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.delete_vertices(**vars_dict)
    process_output(output, select, response)


@workflow.command('get_forecast', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value calendarid=value calendarname=value triggerid=value triggername=value date=value time=value timezone=value forecast_timezone=value exclude=value variable=value')
@click.pass_obj
@output_option
@select_option
def get_forecast(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_forecast(**vars_dict)
    process_output(output, select, response)



def run():
    main()

if __name__ == '__main__':
    main()