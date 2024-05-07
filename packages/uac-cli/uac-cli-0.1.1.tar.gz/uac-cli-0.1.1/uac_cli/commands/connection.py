import click
from uac_cli.utils.process import process_output, process_input, create_payload
from uac_cli.utils.options import output_option, input_option, select_option, ignore_ids

@click.group(help='Parent group for connection-related commands, serving as a namespace for database, email, and other connection types.')
def connection():
    pass

@connection.group(help='Commands related to database connections, including listing, creating, and updating database connection details.')
def database():
    pass

@connection.group(help='Commands for managing email connections, allowing users to create, update, and delete email connection configurations.')
def email():
    pass

@connection.group(help='Commands for managing PeopleSoft connections, including operations to create, update, and delete PeopleSoft connection details.')
def peoplesoft():
    pass

@connection.group(help='Commands related to SAP connections, including operations for managing SAP connection configurations.')
def sap():
    pass


@database.command('get', short_help='Retrieves information on a specific Database Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_database_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.get_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('update', short_help='Modifies the Database Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value db_type=value db_url=value db_driver=value db_max_rows=value db_description=value credentials=value retain_sys_ids=value opswise_groups=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_database_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.databaseconnections.update_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('create', short_help='Creates a Database Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_database_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.databaseconnections.create_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('delete', short_help='Deletes the specified Database Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_database_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.delete_database_connection(**vars_dict)
    process_output(output, select, response)


@database.command('list', short_help='Retrieves information on all Database Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_database_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.databaseconnections.list_database_connections(**vars_dict)
    process_output(output, select, response)


@email.command('get', short_help='Retrieves information on a specific Email Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_email_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.get_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('update', short_help='Modifies the Email Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value smtp=value smtp_port=value smtp_ssl=value smtp_starttls=value email_addr=value default_user=value default_pwd=value authentication=value authentication_type=value oauth_client=value system_connection=value type=value imap=value imap_port=value imap_ssl=value imap_starttls=value trash_folder=value opswise_groups=value description=value authorized=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_email_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.emailconnections.update_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('create', short_help='Creates an Email Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_email_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.emailconnections.create_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('delete', short_help='Deletes the specified Email Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_email_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.delete_email_connection(**vars_dict)
    process_output(output, select, response)


@email.command('list', short_help='Retrieves information on all Email Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_email_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.emailconnections.list_email_connections(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('get', short_help='Retrieves information on a specific PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_peoplesoft_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.get_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('update', short_help='Modifies the PeopleSoft Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value description=value server=value port=value endpoint=value credentials=value retain_sys_ids=value opswise_groups=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_peoplesoft_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.peoplesoftconnections.update_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('create', short_help='Creates a PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_peoplesoft_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.peoplesoftconnections.create_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('delete', short_help='Deletes the specified PeopleSoft Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_peoplesoft_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.delete_peoplesoft_connection(**vars_dict)
    process_output(output, select, response)


@peoplesoft.command('list', short_help='Retrieves information on all PeopleSoft Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_peoplesoft_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.peoplesoftconnections.list_peoplesoft_connections(**vars_dict)
    process_output(output, select, response)



@sap.command('get', short_help='Retrieves information on a specific SAP Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def get_sap_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.get_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('update', short_help='Modifies the SAP Connection specified by the sysId.')
@click.argument('args', nargs=-1, metavar='version=value sys_id=value exclude_related=value export_release_level=value export_table=value name=value sap_connection_type=value sap_ashost=value sap_client=value sap_sysnr=value sap_gwhost=value sap_gwserv=value sap_r3name=value sap_mshost=value sap_group=value opswise_groups=value description=value sap_saprouter=value sap_snc_mode=value sap_snc_lib=value sap_snc_myname=value sap_snc_partnername=value sap_snc_qop=value sap_snc_sso=value sap_mysapsso2=value sap_x509cert=value sap_use_symbolic_names=value retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
def update_sap_connection(uac, args, output=None, input=None, select=None):
    vars_dict = process_input(args, input)
    response = uac.sapconnections.update_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('create', short_help='Creates an SAP Connection.')
@click.argument('args', nargs=-1, metavar='retain_sys_ids=value')
@click.pass_obj
@output_option
@input_option
@select_option
@ignore_ids
def create_sap_connection(uac, args, output=None, input=None, select=None, ignore_ids=False):
    vars_dict = process_input(args, input, ignore_ids)
    response = uac.sapconnections.create_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('delete', short_help='Deletes the specified SAP Connection.')
@click.argument('args', nargs=-1, metavar='connectionid=value connectionname=value')
@click.pass_obj
@output_option
@select_option
def delete_sap_connection(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.delete_sap_connection(**vars_dict)
    process_output(output, select, response)


@sap.command('list', short_help='Retrieves information on all SAP Connections.')
@click.argument('args', nargs=-1, metavar='')
@click.pass_obj
@output_option
@select_option
def list_sap_connections(uac, args, output=None, select=None):
    vars_dict = process_input(args)
    response = uac.sapconnections.list_sap_connections(**vars_dict)
    process_output(output, select, response)
