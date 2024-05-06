import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Commands for managing cluster nodes, including retrieving information about the current node.')
def cluster_node():
    pass


@cluster_node.command('get', short_help='Retrieves information on the current Cluster Node.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def get_cluster_node(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.cluster_nodes.get_cluster_node(**vars_dict)
    process_output(output, select, response)


@cluster_node.command('list', short_help='Retrieves information on all Cluster Nodes.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_cluster_nodes(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.cluster_nodes.list_cluster_nodes(**vars_dict)
    process_output(output, select, response)