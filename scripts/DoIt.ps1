function New-PSVsts {
    function upperFirst {
        param([string]$target)
        "{0}{1}" -f $target[0].ToString().ToUpper(), $target.Substring(1)
    }

    $cli="$args"
    $functionName = "Invoke-Vsts"
    $functionName += ($args | ForEach-Object {upperFirst ($_.replace("-","")) }) -join ''


@"
<#
    .SYNOPSIS
      Short
    .DESCRIPTION
      Long
#>
function $functionName {
    param()

    $("vsts {0}" -f $cli)
}

"@

}

python .\generate_ps_command.py | ForEach-Object { "New-PSVsts $($_)" | Invoke-Expression } | Set-Content .\vsts.psm1
