import click
import colorama

def init_cli():
    click.echo(f'=======================================================================================================================')
    click.echo(f'                                                  SQL Unit Test                                                        ')
    click.echo(f'=======================================================================================================================')
    click.echo(f'                                                                                                                       ')

def report_file_count(files_list):
    click.echo(f'                                                                                                                       ')
    click.echo(colorama.Fore.BLUE + f'                                                 Running {len(files_list)} test(s)                                      ')
    click.echo(f'                                                                                                                       ')
    
def report_test_start(filename, index=0):
    click.echo(colorama.Fore.WHITE + f'                 test {index + 1}: {filename}                                                  ')

def report_passing_test_result(test_duration):
    click.echo(colorama.Fore.GREEN + f'                    PASS' + colorama.Fore.LIGHTWHITE_EX  + f' [{test_duration} second(s)]                                      ')

def report_failing_test_result(test_file_path: str, test_duration, failure_file_path):
    click.echo(colorama.Fore.RED + f'                    FAIL' + colorama.Fore.LIGHTWHITE_EX  + f' [{test_duration} second(s)]                                      ')
    click.echo(colorama.Fore.BLUE + f'                    failure file: {failure_file_path}                           ')
    click.echo(colorama.Fore.BLUE + f'                    test file: {test_file_path}                 ')

def report_missing_uri():
    click.echo(colorama.Fore.RED + f'                    Error: No database URI was provided. Add one to the sql-unit-test.yaml file or pass the --uri option to sql-unit-test')

def report_invalid_uri(exception):
    click.echo(colorama.Fore.RED + f'                    Error: The database URI that was provided is not valid.\n                    Error msg from sqlalchemy: {exception}')
    click.echo(f'                                                                                                                       ')

def report_non_sql_filetype(filename):
    click.echo(colorama.Fore.RED + f'                    Error: {filename} is not a sql file.                                       ')
    click.echo(colorama.Fore.WHITE + f'                                                                                             ')

def report_test_sql_query_error(exception):
    click.echo(colorama.Fore.RED + f'                    Error: Issue running unit test sql query. \n                    Exception msg: {exception}                                       ')
    click.echo(colorama.Fore.WHITE + f'                                                                                             ')

def report_successful_project_initialization(cwd):
    click.echo(f'                                                                                                                       ')
    click.echo(colorama.Fore.GREEN + f'                              Project successfully initialized in {cwd}!                                               ')

