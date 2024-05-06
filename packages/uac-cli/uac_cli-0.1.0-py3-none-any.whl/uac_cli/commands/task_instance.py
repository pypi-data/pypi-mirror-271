import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing task instances, including listing, updating, and controlling the execution of task instances.')
def task_instance():
    pass

@task_instance.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def delete_task_instance(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.delete_task_instance(**vars_dict)
    process_output(output, select, response)


@task_instance.command('show_variables', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value fetchglobal=value')
@click.pass_obj
@output_option
@select_option
def show_variables(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.show_variables(**vars_dict)
    process_output(output, select, response)


@task_instance.command('update_operational_memo', short_help='None')
@click.argument('args', nargs=-1, metavar='memo=message taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_operational_memo(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.task_instances.update_operational_memo(**vars_dict)
    process_output(output, select, response)


@task_instance.command('set_priority', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_set_priority(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_priority(**vars_dict)
    process_output(output, select, response)

@task_instance.command('set_complete', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value operationalMemo=value')
@click.pass_obj
@output_option
@select_option
def task_instance_set_priority(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_complete(**vars_dict)
    process_output(output, select, response)


@task_instance.command('set_timewait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def set_timewait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.set_timewait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('list_dependency_list', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value dependencytype=value')
@click.pass_obj
@output_option
@select_option
def list_dependency_list(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.list_dependency_list(**vars_dict)
    process_output(output, select, response)


@task_instance.command('task_insert', short_help='None')
@click.argument('args', nargs=-1, metavar='id=value name=value alias=value workflow_instance_id=value workflow_instance_name=value workflow_instance_criteria=value predecessors=value successors=value vertex_x=value vertex_y=value inherit_trigger_time=value')
@click.pass_obj
@output_option
@select_option
def task_insert(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    if "predecessors" in vars_dict:
        vars_dict["predecessors"] = vars_dict["predecessors"].split(",")
    if "successors" in vars_dict:
        vars_dict["successors"] = vars_dict["successors"].split(",")
    response = uac.task_instances.task_insert(**vars_dict)
    process_output(output, select, response)


@task_instance.command('cancel', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_cancel(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.cancel(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_dependencies', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_dependencies(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_dependencies(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_exclusive', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_exclusive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_exclusive(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_instance_wait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_instance_wait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_instance_wait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_predecessors', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_predecessors(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_predecessors(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_resources', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_resources(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_resources(**vars_dict)
    process_output(output, select, response)


@task_instance.command('clear_timewait', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_clear_timewait(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.clear_timewait(**vars_dict)
    process_output(output, select, response)


@task_instance.command('force_finish', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_force_finish(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.force_finish(**vars_dict)
    process_output(output, select, response)


@task_instance.command('force_finish_cancel', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_force_finish_cancel(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.force_finish_cancel(**vars_dict)
    process_output(output, select, response)


@task_instance.command('hold', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_hold(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.hold(**vars_dict)
    process_output(output, select, response)


@task_instance.command('release', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_release(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.release(**vars_dict)
    process_output(output, select, response)


@task_instance.command('rerun', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_rerun(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.rerun(**vars_dict)
    process_output(output, select, response)


@task_instance.command('retrieve_output', short_help='None')
@click.argument('args', nargs=-1, metavar='taskinstancename=value taskinstanceid=value workflowinstancename=value criteria=value outputtype=value startline=value numlines=value scantext=value operational_memo=value')
@click.pass_obj
@output_option
@select_option
def task_instance_retrieve_output(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.retrieve_output(**vars_dict)
    process_output(output, select, response)


@task_instance.command('skip', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_skip(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.skip(**vars_dict)
    process_output(output, select, response)


@task_instance.command('skip_path', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value')
@click.pass_obj
@output_option
@select_option
def task_instance_skip_path(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.skip_path(**vars_dict)
    process_output(output, select, response)


@task_instance.command('unskip', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value')
@click.pass_obj
@output_option
@select_option
def task_instance_unskip(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.unskip(**vars_dict)
    process_output(output, select, response)


@task_instance.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='name=value id=value criteria=value workflow_instance_name=value resource_name=value recursive=value predecessor_name=value wait_type=value wait_time=value wait_duration=value wait_seconds=value wait_day_constraint=value delay_type=value delay_duration=value delay_seconds=value halt=value priority_type=value task_status=value operational_memo=value hold_reason=value agent_name=value workflow_instance_criteria=value workflow_instance_id=value status=value type=value execution_user=value late_start=value late_finish=value early_finish=value started_late=value finished_late=value finished_early=value late=value late_early=value business_services=value updated_time_type=value updated_time=value sys_id=value instance_number=value task_id=value task_name=value custom_field1=value custom_field2=value trigger_id=value trigger_name=value workflow_definition_id=value workflow_definition_name=value status_description=value template_id=value template_name=value response_fields=value instance_output_type=value')
@click.pass_obj
@output_option
@select_option
def list_status(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.task_instances.list_status(**vars_dict)
    process_output(output, select, response)

