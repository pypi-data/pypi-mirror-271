import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands related to universal events, including publishing and managing universal events.')
def universal_event():
    pass

@universal_event.command('publish', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value business_services=value ttl=value attributes=value')
@click.pass_obj
@output_option
@select_option
def publish(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.publish(**vars_dict)
    process_output(output, select, response)


@universal_event.command('pushg', short_help='None')
@click.argument('args', nargs=-1, metavar='payload=value')
@click.pass_obj
@output_option
@select_option
def pushg(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.pushg(**vars_dict)
    process_output(output, select, response)


@universal_event.command('push', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def push(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_events.push(**vars_dict)
    process_output(output, select, response)

