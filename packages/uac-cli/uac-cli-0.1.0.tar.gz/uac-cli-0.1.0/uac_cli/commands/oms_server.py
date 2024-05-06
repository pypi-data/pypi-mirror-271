import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids


@click.group(help='Commands related to OMS servers, including listing, creating, updating, and deleting OMS server configurations.')
def oms_server():
    pass

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
