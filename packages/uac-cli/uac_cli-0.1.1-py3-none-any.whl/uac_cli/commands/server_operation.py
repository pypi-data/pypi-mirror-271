import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for server operations, such as log rolling and temporary property changes.')
def server_operation():
    pass

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
