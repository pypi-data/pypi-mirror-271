import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Credential management commands, including creating, updating, deleting, and changing passwords for credentials.')
def credential():
    pass



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