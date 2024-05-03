import click
import colorama

from sql_unit_test.core.run import run
from sql_unit_test.core.initialize import init

colorama.init()

@click.group
def my_commands():
    pass

my_commands.add_command(run)
my_commands.add_command(init)

            
if __name__ == "__main__":
    my_commands()
