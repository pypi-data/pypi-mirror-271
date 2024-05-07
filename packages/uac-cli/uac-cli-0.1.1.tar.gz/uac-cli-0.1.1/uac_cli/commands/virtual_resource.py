import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands related to virtual resources, including listing, creating, updating, and deleting virtual resources.')
def virtual_resource():
    pass


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

