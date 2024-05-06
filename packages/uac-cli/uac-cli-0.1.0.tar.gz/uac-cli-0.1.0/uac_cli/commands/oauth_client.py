import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing OAuth clients, including creating, updating, and listing OAuth clients.')
def oauth_client():
    pass



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

