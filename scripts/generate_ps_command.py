from __future__ import print_function

import sys
import os

from knack import CLI
from vsts.cli.vsts_cli_help import VstsCLIHelp
from vsts.cli.vsts_commands_loader import VstsCommandsLoader

cmd_set_names = None
param_names = None

cli_name = "vsts"
vstscli = CLI(cli_name=cli_name,
        config_dir=os.path.join('~', '.{}'.format(cli_name)),
        config_env_var_prefix=cli_name,
        commands_loader_cls=VstsCommandsLoader,
        help_cls=VstsCLIHelp)

loader = vstscli.commands_loader_cls()
loader.__init__(vstscli)
#loader.load_command_table([])

cmd_table = loader.load_command_table([])
for command in loader.command_table:
    loader.load_arguments(command)

cmd_list = [cmd_name for cmd_name in cmd_table.keys() if cmd_set_names is None or cmd_name.split()[0] in cmd_set_names]
results = []

print('"command","arg"')
for name in cmd_list:
    cmd_name = [x for x in cmd_table.keys() if name == x][0]
    cmd_args = cmd_table[cmd_name].arguments
    for arg in cmd_args:
        print('"' + cmd_name + '","' + arg + '"')