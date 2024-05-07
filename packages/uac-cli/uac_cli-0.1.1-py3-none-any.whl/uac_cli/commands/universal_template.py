import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing universal templates, including template creation, deletion, and updating.')
def universal_template():
    pass


@universal_template.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_universal_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.get_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('update', short_help='None')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value extension=value variable_prefix=value log_level=value icon_filename=value icon_filesize=value icon_date_created=value template_type=value agent_type=value use_common_script=value script=value script_unix=value script_windows=value script_type_windows=value always_cancel_on_finish=value send_variables=value credentials=value credentials_var=value credentials_var_check=value agent=value agent_var=value agent_var_check=value agent_cluster=value agent_cluster_var=value agent_cluster_var_check=value broadcast_cluster=value broadcast_cluster_var=value broadcast_cluster_var_check=value runtime_dir=value environment=value send_environment=value exit_codes=value exit_code_processing=value exit_code_text=value exit_code_output=value output_type=value output_content_type=value output_path_expression=value output_condition_operator=value output_condition_value=value output_condition_strategy=value auto_cleanup=value output_return_type=value output_return_file=value output_return_sline=value output_return_nline=value output_return_text=value wait_for_output=value output_failure_only=value elevate_user=value desktop_interact=value create_console=value agent_fields_restriction=value credential_fields_restriction=value environment_variables_fields_restriction=value exit_code_processing_fields_restriction=value automatic_output_retrieval_fields_restriction=value retain_sys_ids=value min_release_level=value environment_from_string=value fields=value commands=value events=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_universal_template(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.universal_templates.update_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('create', short_help='None')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_universal_template(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.universal_templates.create_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('delete', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_universal_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.delete_universal_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('get', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def get_extension_archive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.get_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('update_extension_archive', short_help='None')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@input_option
@select_option
def update_extension_archive(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.universal_templates.update_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('delete_extension_archive', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def delete_extension_archive(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.delete_extension_archive(**vars_dict)
    process_output(output, select, response)


@universal_template.command('export', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value exclude_extension=value')
@click.pass_obj
@output_option
@select_option
def export_template(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.export_template(**vars_dict)
    process_output(output, select, response)


@universal_template.command('set_icon', short_help='None')
@click.argument('args', nargs=-1, metavar='templateid=value templatename=value')
@click.pass_obj
@output_option
@select_option
def set_template_icon(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.set_template_icon(**vars_dict)
    process_output(output, select, response)


@universal_template.command('list', short_help='None')
@click.argument('args', nargs=-1, metavar='templatename=value')
@click.pass_obj
@output_option
@select_option
def list_universal_templates(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.universal_templates.list_universal_templates(**vars_dict)
    process_output(output, select, response)

