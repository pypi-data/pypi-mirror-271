import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing agents, such as retrieving, updating, and deleting agents.')
def agent():
    pass

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