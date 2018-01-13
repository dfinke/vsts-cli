# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import argparse
import json
import re
import sys
import os
# from knack import CLI
from vsts.cli.vsts_cli_help import VstsCLIHelp
from vsts.cli.vsts_commands_loader import VstsCommandsLoader

class Exporter(json.JSONEncoder):

    def default(self, o):#pylint: disable=method-hidden
        try:
            return super(Exporter, self).default(o)
        except TypeError:
            return str(o)


def _store_parsers(parser, parser_keys, parser_values, sub_parser_keys, sub_parser_values):
    for s in parser.subparsers.values():
        parser_keys.append(_get_parser_name(s))
        parser_values.append(s)
        if _is_group(s):
            for c in s.choices.values():
                sub_parser_keys.append(_get_parser_name(c))
                sub_parser_values.append(c)
                _store_parsers(c, parser_keys, parser_values,
                               sub_parser_keys, sub_parser_values)


def _load_doc_source_map():
    with open('docgen\doc_source_map.json') as open_file:
        return json.load(open_file)


def _is_group(parser):
    return getattr(parser, '_subparsers', None) is not None \
        or getattr(parser, 'choices', None) is not None


def _get_parser_name(s):
    return (s._prog_prefix if hasattr(s, '_prog_prefix') else s.prog)[5:]

parser_keys = []
parser_values = []
sub_parser_keys = []
sub_parser_values = []

parser = argparse.ArgumentParser(description='Command Table Parser')
parser.add_argument('--commands', metavar='N', nargs='+', help='Filter by first level command (OR)') #, default='build')
parser.add_argument('--params', metavar='N', nargs='+', help='Filter by parameters (OR)') #, default='list')
args = parser.parse_args()
cmd_set_names = args.commands
param_names = args.params

# ignore the params passed in now so they aren't used by the cli
sys.argv = sys.argv[:1]

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

vstsclihelp = vstscli.help_cls(cli_ctx=vstscli)

global_parser = vstscli.parser_cls.create_global_parser(
    cli_ctx=vstscli)
parser = vstscli.parser_cls(
    cli_ctx=vstscli, prog=vstscli.name, parents=[global_parser])
parser.load_command_table(loader.command_table)

_store_parsers(parser, parser_keys, parser_values,
                       sub_parser_keys, sub_parser_values)

doc_source_map = _load_doc_source_map()

help_files = []
for cmd, parser in zip(sub_parser_keys, sub_parser_values):
    try:
        print(cmd)
        # help_file = _help.GroupHelpFile(cmd, parser) if _is_group(
        #     parser) else _help.CommandHelpFile(cmd, parser)
        # help_file.load(parser)
        # help_files.append(help_file)
    except Exception as ex:
        print("Skipped '{}' due to '{}'".format(cmd, ex))
help_files = sorted(help_files, key=lambda x: x.command)

# cmd_list = [cmd_name for cmd_name in cmd_table.keys() if cmd_set_names is None or cmd_name.split()[0] in cmd_set_names]
# results = []

# print('"command","arg"')
# for name in cmd_list:
#     cmd_name = [x for x in cmd_table.keys() if name == x][0]
#     #print(cmd_name)
#     cmd_args = cmd_table[cmd_name].arguments
#     for arg in cmd_args:
#         print('"' + cmd_name + '","' + arg + '"')



# if param_names:
#     for name in cmd_list:
#         cmd_name = [x for x in cmd_table.keys() if name == x][0]
#         cmd_args = cmd_table[cmd_name].arguments
#         match = False
#         for arg in cmd_args:
#             if match:
#                 break
#             arg_name = re.sub('--','', arg['name']).split(' ')[0]
#             if arg_name in param_names:
#                 results.append(name)
#                 match = True
# else:
#     results = cmd_list

# heading = '=== COMMANDS IN {} PACKAGE(S) WITH {} PARAMETERS ==='.format(
#     cmd_set_names or 'ANY', param_names or 'ANY')
# print('\n{}\n'.format(heading))
# print('\n'.join(results))

# #heading = '=== COMMANDS IN {} PACKAGE(S) WITH {} PARAMETERS ==='.format(cmd_set_names or 'ANY', param_names or 'ANY')
# #heading = '=== PowerShell Time ==='.format(cmd_set_names or 'ANY', param_names or 'ANY')
# #print('\n{}\n'.format(heading))
# # print('\n'.join(results))

# # print(results)
# #print(results)

# #print(cmd_table['build list']['arguments'])
# #print(cmd_table.keys())
