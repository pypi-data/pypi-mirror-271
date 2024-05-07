import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='System-related commands, including retrieving system status and information.')
@click.pass_obj
def system(uac):
    if uac is None:
        click.echo(click.style("No profiles found. run `uac config init`", fg="bright_red"))
        exit(255)

@system.command('get', short_help='None')
@click.pass_obj
@output_option
@select_option
def get_status(uac, output=None, select=None):
    response = uac.system.get_status()
    process_output(output, select, response)
