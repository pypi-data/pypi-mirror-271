import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing triggers, including creating, updating, and listing triggers.')
def trigger():
    pass


@trigger.command('list_qualifying_times', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value count=value startdate=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_times(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_qualifying_times(**vars_dict)
    process_output(output, select, response)


@trigger.command('unassign_execution_user', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def unassign_execution_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.unassign_execution_user(**vars_dict)
    process_output(output, select, response)

@trigger.command('assign_execution_user', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value username=username password=password')
@click.pass_obj
@output_option
@select_option
def unassign_execution_user(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.assign_execution_user_to_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_temp_trigger(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.triggers.create_temp_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def get_trigger(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.get_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value name=value description=value calendar=value enabled=value forecast=value restriction=value restriction_simple=value restriction_complex=value situation=value action=value restriction_mode=value restriction_adjective=value restriction_nth_amount=value restriction_noun=value restriction_nouns=value restriction_qualifier=value restriction_qualifiers=value skip_count=value skip_active=value simulation_option=value time_zone=value execution_user=value opswise_groups=value tasks=value retention_duration_purge=value retention_duration=value retention_duration_unit=value rd_exclude_backup=value skip_condition=value skip_restriction=value skip_after_date=value skip_after_time=value skip_before_date=value skip_before_time=value skip_date_list=value enabled_by=value enabled_time=value disabled_by=value disabled_time=value next_scheduled_time=value enforce_variables=value lock_variables=value custom_field1=value custom_field2=value variables=value notes=value restriction_qualifiers_from_string=value restriction_nouns_from_string=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_trigger(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.triggers.update_trigger(**vars_dict)
    process_output(output, select, response)

@trigger.command('enable_disable', short_help='None')
@click.argument('args', nargs=-1, metavar='enable=boolean name=triggername')
@click.pass_obj
@output_option
@input_option
@select_option
def enable_disable(uac, args, output=None, input=None, select=None):
    _payload = [create_payload(args)]
    response = uac.triggers.enable_disable(payload=_payload)
    process_output(output, select, response)


@trigger.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_trigger(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.triggers.create_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='triggerid=value triggername=value')
@click.pass_obj
@output_option
@select_option
def delete_trigger(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.delete_trigger(**vars_dict)
    process_output(output, select, response)


@trigger.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value enabled=value type=value business_services=value updated_time_type=value updated_time=value workflow_id=value workflow_name=value agent_name=value description=value tasks=value template_id=value template_name=value')
@click.pass_obj
@output_option
@select_option
def list_triggers(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_triggers(**vars_dict)
    process_output(output, select, response)


@trigger.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='triggername=value type=value business_services=value enabled=value tasks=value description=value')
@click.pass_obj
@output_option
@select_option
def list_triggers_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.triggers.list_triggers_advanced(**vars_dict)
    process_output(output, select, response)

