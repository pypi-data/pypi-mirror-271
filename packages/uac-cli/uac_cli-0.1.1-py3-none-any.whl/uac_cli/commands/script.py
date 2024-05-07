import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Script management commands, including creating, updating, deleting, and listing scripts.')
def script():
    pass

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
