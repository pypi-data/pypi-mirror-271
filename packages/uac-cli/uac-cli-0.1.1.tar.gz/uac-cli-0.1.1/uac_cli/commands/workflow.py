import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids


@click.group(help='Workflow management commands, including operations for managing workflow vertices and edges, as well as running workflow forecasts.')
def workflow():
    pass



@workflow.command('get_edges', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value sourceid=value targetid=value')
@click.pass_obj
@output_option
@select_option
def get_edges(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_edges(**vars_dict)
    process_output(output, select, response)


@workflow.command('update_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='sys_id=value workflow_id=value condition=value straight_edge=value points=value source_id=value target_id=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_edge(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.workflows.update_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('add_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value condition=value straight_edge=value points=value source_id=value target_id=value')
@click.pass_obj
@output_option
@select_option
def add_edge(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('delete_edge', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value sourceid=value targetid=value')
@click.pass_obj
@output_option
@select_option
def delete_edge(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.delete_edge(**vars_dict)
    process_output(output, select, response)


@workflow.command('get_vertices', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value taskid=value taskname=value taskalias=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def get_vertices(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_vertices(**vars_dict)
    process_output(output, select, response)


@workflow.command('update_vertex', short_help='None')
@click.argument('args', nargs=-1, metavar='sys_id=value workflow_id=value task=value alias=value vertex_id=value vertex_x=value vertex_y=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_vertex(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.workflows.update_vertex(**vars_dict)
    process_output(output, select, response)


@workflow.command('add_vertex', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value task=value alias=value vertex_id=value vertex_x=value vertex_y=value')
@click.pass_obj
@output_option
@select_option
def add_vertex(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_vertex(**vars_dict)
    process_output(output, select, response)

@workflow.command('add_child_vertex', short_help='Adds a vertex and edge')
@click.argument('args', nargs=-1, metavar='workflow_name=value parent_task_name=name parent_vertex_id=[optional] task_name=new_task vertex_id=[optional] vertexX=None vertexY=None vertex_x_offset=100 vertex_y_offset=100')
@click.pass_obj
@output_option
@select_option
def add_child_vertex(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.add_child_vertex(**vars_dict)
    process_output(output, select, response)


@workflow.command('delete_vertices', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value taskid=value taskname=value taskalias=value vertexid=value')
@click.pass_obj
@output_option
@select_option
def delete_vertices(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.delete_vertices(**vars_dict)
    process_output(output, select, response)


@workflow.command('get_forecast', short_help='None')
@click.argument('args', nargs=-1, metavar='workflowid=value workflowname=value calendarid=value calendarname=value triggerid=value triggername=value date=value time=value timezone=value forecast_timezone=value exclude=value variable=value')
@click.pass_obj
@output_option
@select_option
def get_forecast(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.workflows.get_forecast(**vars_dict)
    process_output(output, select, response)