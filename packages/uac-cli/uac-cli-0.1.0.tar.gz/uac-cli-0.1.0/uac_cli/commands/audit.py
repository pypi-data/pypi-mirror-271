import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(name='audit', help='Audit commands for retrieving audit logs and information.')
def audit():
    pass

@audit.command('list', short_help='Get a list of audits')
@click.argument('args', nargs=-1, metavar="auditType=auditType source=source status=status createdBy=createdBy tableName=tableName tableRecordName=tableRecordName updatedTimeType=updatedTimeType updatedTime=updatedTime tableKey=tableKey includeChildAudits=includeChildAudits")
@click.pass_obj
@output_option
@select_option
def list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.audits.list_audit(**vars_dict)
    process_output(output, select, response)