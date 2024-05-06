import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Task management commands, including creating, updating, deleting, and launching tasks.')
def task():
    pass


@task.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='taskid=value taskname=value')
@click.pass_obj
@output_option
@select_option
def get_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.get_task(**vars_dict)
    process_output(output, select, response)


@task.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value variables=value notes=value actions=value retain_sys_ids=value name=value resolve_name_immediately=value summary=value opswise_groups=value start_held=value start_held_reason=value res_priority=value hold_resources=value credentials=value credentials_var=value credentials_var_check=value retry_maximum=value retry_indefinitely=value retry_interval=value retry_suppress_failure=value ls_enabled=value ls_type=value ls_time=value ls_day_constraint=value ls_nth_amount=value ls_duration=value lf_enabled=value lf_type=value lf_time=value lf_day_constraint=value lf_nth_amount=value lf_duration=value lf_offset_type=value lf_offset_percentage=value lf_offset_duration=value lf_offset_duration_unit=value ef_enabled=value ef_type=value ef_time=value ef_day_constraint=value ef_nth_amount=value ef_duration=value ef_offset_type=value ef_offset_percentage=value ef_offset_duration=value ef_offset_duration_unit=value user_estimated_duration=value cp_duration=value cp_duration_unit=value tw_wait_type=value tw_wait_amount=value tw_wait_time=value tw_wait_duration=value tw_wait_day_constraint=value tw_delay_type=value tw_delay_amount=value tw_delay_duration=value tw_workflow_only=value custom_field1=value custom_field2=value execution_restriction=value restriction_period=value restriction_period_before_date=value restriction_period_after_date=value restriction_period_before_time=value restriction_period_after_time=value restriction_period_date_list=value log_level=value exclusive_with_self=value min_run_time=value max_run_time=value avg_run_time=value last_run_time=value min_run_time_display=value max_run_time_display=value avg_run_time_display=value last_run_time_display=value run_count=value run_time=value first_run=value last_run=value simulation=value enforce_variables=value lock_variables=value override_instance_wait=value time_zone_pref=value virtual_resources=value exclusive_tasks=value type=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_task(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.tasks.update_task(**vars_dict)
    process_output(output, select, response)


@task.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_task(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.tasks.create_task(**vars_dict)
    process_output(output, select, response)


@task.group(name='new', short_help='Create new tasks from template.')
def new_task():
    pass


@new_task.command('linux', short_help='Create new Linux tasks from template.')
@click.argument('args', nargs=-1, metavar='name=taskname agent=agent_name command=[command to execute] script=[name of the script to execute]' )
@click.pass_obj
@output_option
@select_option
def linux_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_linux_task(**vars_dict)
    process_output(output, select, response)

@new_task.command('windows', short_help='Create new Windows tasks from template.')
@click.argument('args', nargs=-1, metavar='name=taskname agent=agent_name command=[command to execute] script=[name of the script to execute]' )
@click.pass_obj
@output_option
@select_option
def linux_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_windows_task(**vars_dict)
    process_output(output, select, response)

@new_task.command('workflow', short_help='Create new Workflow tasks from template.')
@click.argument('args', nargs=-1, metavar='name=[workflow name]' )
@click.pass_obj
@output_option
@select_option
def workflow_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.create_workflow(**vars_dict)
    process_output(output, select, response)

@task.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='taskid=value taskname=value')
@click.pass_obj
@output_option
@select_option
def delete_task(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.delete_task(**vars_dict)
    process_output(output, select, response)


@task.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value enabled=value type=value business_services=value updated_time_type=value updated_time=value workflow_id=value workflow_name=value agent_name=value description=value tasks=value template_id=value template_name=value')
@click.pass_obj
@output_option
@select_option
def list_tasks(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_tasks(**vars_dict)
    process_output(output, select, response)


@task.command('list_advanced', short_help='None')
@click.argument('args', nargs=-1, metavar='taskname=value agentname=value type=value business_services=value workflowname=value workflowid=value updated_time=value updated_time_type=value templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def list_tasks_advanced(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_tasks_advanced(**vars_dict)
    process_output(output, select, response)


@task.command('list_workflow_list', short_help='None')
@click.argument('args', nargs=-1, metavar='taskname=value taskid=value')
@click.pass_obj
@output_option
@select_option
def list_workflow_list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_workflow_list(**vars_dict)
    process_output(output, select, response)


@task.command('list_dependency_list_1', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value dependencytype=value')
@click.pass_obj
@output_option
@select_option
def list_dependency_list_1(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.tasks.list_dependency_list_1(**vars_dict)
    process_output(output, select, response)


@task.command('launch', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value hold=value hold_reason=value time_zone=value virtual_resource_priority=value virtual_resources=value launch_reason=value simulate=value variables=value variables_map=value')
@click.pass_obj
@output_option
@select_option
@click.option('--wait', '-w', is_flag=True)
@click.option('--timeout', '-t', type=int, default=300)
@click.option('--interval', '-i', type=int, default=10)
@click.option('--return_rc', '-r', is_flag=True)
def task_launch(uac, args, output=None, select=None, wait=False, timeout=300, interval=10, return_rc=False):
    vars_dict = process_input(args)
    if wait:
        response = uac.tasks.task_launch_and_wait(timeout=timeout, interval=interval, **vars_dict)
    else:
        response = uac.tasks.task_launch(**vars_dict)
    process_output(output, select, response)
    if wait and return_rc:
        if "exitCode" in response:
            exit(int(response["exitCode"]))
        else:
            if response.get("status", "UNKNOWN") in uac.task_instances.SUCCESS_STATUSES:
                exit(0)
            else:
                exit(1)


