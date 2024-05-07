import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Calendar-related commands for managing calendars and custom days within them.')
def calendar():
    pass


@calendar.command('get', short_help='Retrieves information on all Custom Days of a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def get_custom_days(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.get_custom_days(**vars_dict)
    process_output(output, select, response)


@calendar.command('add', short_help='Adds the specified Custom Day to the specified Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def add_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.add_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('remove', short_help='Removes the specified Custom Day from a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value customdayid=value customdayname=value')
@click.pass_obj
@output_option
@select_option
def remove_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.remove_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('get', short_help='Retrieves information on a specific Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def get_calendar(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.get_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('update', short_help='Modifies the Calendar specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value comments=value opswise_groups=value business_days=value first_quarter_start=value second_quarter_start=value third_quarter_start=value fourth_quarter_start=value retain_sys_ids=value first_day_of_week=value custom_days=value local_custom_days=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_calendar(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.calendars.update_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('create', short_help='Creates a new Calendar.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_calendar(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.calendars.create_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('delete', short_help='Deletes the specified Calendar.')
@click.argument('args', nargs=-1, metavar='calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def delete_calendar(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.delete_calendar(**vars_dict)
    process_output(output, select, response)


@calendar.command('list', short_help='Retrieves information on all Calendars.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_calendars(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_calendars(**vars_dict)
    process_output(output, select, response)


@calendar.command('list_qualifying_dates_for_local_custom_day', short_help='Retrieves information on Qualifying Dates for a specific Local Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayname=value calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_dates_for_local_custom_day(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_qualifying_dates_for_local_custom_day(**vars_dict)
    process_output(output, select, response)


@calendar.command('list_qualifying_periods', short_help='Retrieves information on Qualifying Periods for a specific Local Custom Day.')
@click.argument('args', nargs=-1, metavar='customdayname=value calendarid=value calendarname=value')
@click.pass_obj
@output_option
@select_option
def list_qualifying_periods(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.calendars.list_qualifying_periods(**vars_dict)
    process_output(output, select, response)
