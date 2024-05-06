import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Property management commands, allowing users to list, create, update, and delete properties.')
def property():
    pass


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
