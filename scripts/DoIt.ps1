function Invoke-UpperCaseFirstLetter {
    param([string]$target)

    $target.Substring(0, 1).ToUpper() + $target.Substring(1)
}

function ConvertTo-PSFunction {
    [CmdletBinding()]
    param(
        [Switch]$Evaluate,
        [Switch]$SaveToPSM1
    )

    $r = python .\generate_ps_command.py | ConvertFrom-Csv | Group-Object command

    $result = foreach ($record in $r) {
        $parts = $record.name.split(' ')

        $fnPart = switch ($parts.count) {
            1 {"Vsts{0}" -f (Invoke-UpperCaseFirstLetter $parts[0])}
            2 {"Vsts{0}" -f (Invoke-UpperCaseFirstLetter $parts[0])}
            3 {"Vsts{0}{1}" -f (Invoke-UpperCaseFirstLetter $parts[0]), (Invoke-UpperCaseFirstLetter $parts[1])}
            4 {"Vsts{0}{1}{2}" -f (Invoke-UpperCaseFirstLetter $parts[0]), (Invoke-UpperCaseFirstLetter $parts[1]), (Invoke-UpperCaseFirstLetter $parts[2])}
        }

        if ($fnPart) {
            $DoConvertFromJson = $false
            if ($parts.Count -eq 1) {
                $functionName = "Invoke-{0}" -f ($fnPart -replace "-", "")
            }
            else {
                $functionName = "{0}-{1}" -f (Invoke-UpperCaseFirstLetter $parts[-1]), ($fnPart -replace "-", "")
                $DoConvertFromJson = $true
            }

            $record |
                Add-Member -PassThru -MemberType NoteProperty -Name FunctionName -Value $functionName -Force |
                Add-Member -PassThru -MemberType NoteProperty -Name DoConvertFromJson -Value $DoConvertFromJson -Force
        }
    }

    $transpile = foreach ($record in $result | Sort-Object FunctionName) {

        $targetExpression = "vsts $($record.name)"
        if ($record.DoConvertFromJson) {
            $targetExpression = "(vsts $($record.name) --output json | ConvertFrom-Json)"
        }
        $params = "`t$" + (($record.group.arg | Sort-Object) -join ",`n`t$")

        @"
function $($record.FunctionName) {
    param(
$($params)
    )

    $targetExpression
}

"@
    }

    if($Evaluate) {
        $transpile | Invoke-Expression
    } elseif($SaveToPSM1) {
        $fileName = "$pwd\vstsPS.psm1"
        $transpile | Set-Content $fileName
        Write-Verbose "Saved to $($fileName)"
    } else {
        $transpile
    }
}

ConvertTo-PSFunction -SaveToPSM1