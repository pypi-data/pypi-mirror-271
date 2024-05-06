import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands to manage business services, enabling operations like listing, creating, and updating business services.')
def business_service():
    pass


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
