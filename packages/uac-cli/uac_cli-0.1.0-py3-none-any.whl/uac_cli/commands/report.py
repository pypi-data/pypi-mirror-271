import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids, output_option_binary

@click.group(help='Commands to run and manage reports, including running reports in various formats.')
def report():
    pass


@report.command('run_report', short_help='None')
@click.argument('args', nargs=-1, metavar='reporttitle=value visibility=value groupname=value format=')
@click.pass_obj
@output_option_binary
@select_option
@click.option("--format", type=click.Choice(["csv", "tab", "pdf", "png", "xml", "json"]))
def run_report(uac, args, output=None, select=None, format="csv"):
    vars_dict = process_input(args)
    response = uac.reports.run_report(report_format=format, **vars_dict)
    process_output(output, select, response, text=True, binary=(format in ["pdf", "png"]))

