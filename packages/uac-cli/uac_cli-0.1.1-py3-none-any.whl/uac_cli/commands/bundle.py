import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Bundle management commands, including operations to list, create, and delete bundles.')
def bundle():
    pass

@click.group(help='Commands related to promotions, including scheduling and managing promotion tasks.')
def promotion():
    pass

@click.group(help='Commands for managing promotion targets, including creating, updating, and deleting promotion targets.')
def promotion_target():
    pass


@bundle.command('promote', short_help='Promote a Bundle or schedule the promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='id=value name=value promotion_target_id=value promotion_target_name=value notification_option=value override_user=value override_password=value date=value time=value schedule=value create_snapshot=value allow_unv_tmplt_changes=value override_token=value')
@click.pass_obj
@output_option
@select_option
def promote(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.promote(**vars_dict)
    process_output(output, select, response)


@bundle.command('get', short_help='Retrieve Bundle details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def get_bundle(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('update', short_help='Modifies the Bundle specified by the sysId.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value name=value sys_id=value description=value opswise_groups=value default_promotion_target=value exclude_on_existence=value follow_references=value promote_bundle_definition=value promote_by_business_services=value visible_to=value bundle_agent_clusters=value bundle_applications=value bundle_business_services=value bundle_calendars=value bundle_credentials=value bundle_custom_days=value bundle_database_connections=value bundle_email_connections=value bundle_email_templates=value bundle_o_auth_clients=value bundle_peoplesoft_connections=value bundle_reports=value bundle_sap_connections=value bundle_scripts=value bundle_snmp_managers=value bundle_tasks=value bundle_triggers=value bundle_universal_event_templates=value bundle_universal_templates=value bundle_variables=value bundle_virtual_resources=value version=value exclude_related=value export_release_level=value export_table=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_bundle(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.bundles.update_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('create', short_help='Creates a Bundle.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_bundle(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('delete', short_help='Deletes the specified Bundle.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def delete_bundle(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_bundle(**vars_dict)
    process_output(output, select, response)


@bundle.command('create_by_date', short_help='Creates a Bundle by Date.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_bundle_by_date(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_bundle_by_date(**vars_dict)
    process_output(output, select, response)


@bundle.command('get_report', short_help='Retrieve Bundle Report details using specific query parameters.')
@click.argument('args', nargs=-1, metavar='bundleid=value bundlename=value')
@click.pass_obj
@output_option
@select_option
def get_bundle_report(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_bundle_report(**vars_dict)
    process_output(output, select, response)


@bundle.command('list', short_help='Retrieves information on all Bundles.')
@click.argument('args', nargs=-1, metavar='bundlename=value business_services=value default_promotion_target=value')
@click.pass_obj
@output_option
@select_option
def list_bundles(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.list_bundles(**vars_dict)
    process_output(output, select, response)



@promotion.command('cancel_promotion_schedule', short_help='Cancels the scheduled promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='scheduleid=value bundleid=value bundlename=value date=value time=value')
@click.pass_obj
@output_option
@select_option
def cancel_promotion_schedule(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.cancel_promotion_schedule(**vars_dict)
    process_output(output, select, response)


@promotion.command('delete', short_help='Deletes the scheduled promotion of a Bundle.')
@click.argument('args', nargs=-1, metavar='scheduleid=value bundleid=value bundlename=value date=value time=value')
@click.pass_obj
@output_option
@select_option
def delete_promotion_schedule(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_promotion_schedule(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('get', short_help='Retrieve a specified Promotion Target details.')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value')
@click.pass_obj
@output_option
@select_option
def get_promotion_target(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.get_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('update', short_help='Modifies the specified Promotion Target.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value retain_sys_ids=value name=value description=value uri=value user=value password=value authentication_method=value opswise_groups=value token=value agent_mappings=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_promotion_target(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.bundles.update_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('create', short_help='Creates a Promotion Target.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_promotion_target(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.bundles.create_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('delete', short_help='Deletes the specified Promotion Target.')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value')
@click.pass_obj
@output_option
@select_option
def delete_promotion_target(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.delete_promotion_target(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('list', short_help='Retrieves information on all Promotion Targets.')
@click.argument('args', nargs=-1, metavar='targetname=value business_services=value')
@click.pass_obj
@output_option
@select_option
def list_promotion_targets(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.list_promotion_targets(**vars_dict)
    process_output(output, select, response)


@promotion_target.command('refresh_target_agents', short_help='None')
@click.argument('args', nargs=-1, metavar='targetname=value targetid=value username=value password=value token=value')
@click.pass_obj
@output_option
@select_option
def refresh_target_agents(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.bundles.refresh_target_agents(**vars_dict)
    process_output(output, select, response)
