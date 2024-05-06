import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids


@click.group(help='User group management commands, including listing, creating, updating, and deleting user groups.')
def user_group():
    pass



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
