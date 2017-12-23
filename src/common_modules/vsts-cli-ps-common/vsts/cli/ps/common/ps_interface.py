# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from knack.commands import CLICommandsLoader
from vsts.cli.build.commands import load_build_commands

# from vsts.cli.common.uri import uri_quote
from datetime import datetime
import datetime

import subprocess

def ps_cvt_work():
    subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "1..10"])
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # xyz = load_build_commands

