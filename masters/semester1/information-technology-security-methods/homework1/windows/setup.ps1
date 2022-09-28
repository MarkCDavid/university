
using namespace System.Security.AccessControl;

#region Identities

function New-ITSMLocalUser {
    param (
        [string]$Name,
        [string[]]$Groups
    )

    $user = New-LocalUser -Name $Name -NoPassword 

    # Has to have one of the Windows system groups, to be able to log into the account
    Add-LocalGroupMember -Group $(Get-LocalGroup -Name "Users") -Member $user | Out-Null 

    foreach($groupName in $Groups) 
    {
        $group = Get-LocalGroup -Name $groupName
        Add-LocalGroupMember -Group $group -Member $user | Out-Null
    }
}

function New-ITSMLocalGroup {
    param (
        [string]$Name
    )

    New-LocalGroup -Name $Name | Out-Null
}
#endregion Identities

#region ICE

function New-ICEFullControl {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        [FileSystemRights]::FullControl, 
        ([InheritanceFlags]::ContainerInherit + [InheritanceFlags]::ObjectInherit), 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ICEReadAndExecute {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        [FileSystemRights]::ReadAndExecute, 
        ([InheritanceFlags]::ContainerInherit + [InheritanceFlags]::ObjectInherit), 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ICEReadExecuteAndWrite {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        ([FileSystemRights]::ReadAndExecute + [FileSystemRights]::Write), 
        ([InheritanceFlags]::ContainerInherit + [InheritanceFlags]::ObjectInherit), 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ICEFullControlContainer {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        [FileSystemRights]::FullControl, 
        [InheritanceFlags]::ContainerInherit, 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ICEReadExecuteAndWriteContainer {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        ([FileSystemRights]::ReadAndExecute + [FileSystemRights]::Write), 
        [InheritanceFlags]::ContainerInherit, 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ICEReadAndExecuteContainer {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        [FileSystemRights]::ReadAndExecute, 
        [InheritanceFlags]::ContainerInherit, 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

#endregion ICE

#region ACL
function Get-ACLDefault {
    param (
        [string]$Path
    )

    $targetAcl = Get-Acl -Path $Path

    $targetAcl.SetAccessRuleProtection($true, $false)

    $creatorSystemIce = New-ICEFullControl -Identifier "NT AUTHORITY\SYSTEM"
    $creatorAdministratorsIce = New-ICEFullControl -Identifier "BUILTIN\Administrators"
    $creatorOwnerIce = New-ICEFullControl -Identifier "CREATOR OWNER"

    $targetAcl.AddAccessRule($creatorSystemIce)
    $targetAcl.AddAccessRule($creatorAdministratorsIce)
    $targetAcl.AddAccessRule($creatorOwnerIce)

    return $targetAcl
}

function Set-ACLRoot {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $sysadminAce = New-ICEFullControl -Identifier "sysadmin"
    $chiefAce = New-ICEFullControl -Identifier "chief"
    $employeeAce = New-ICEReadAndExecuteContainer -Identifier "employee"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)
    $targetAcl.AddAccessRule($employeeAce)

    $targetAcl | Set-Acl -Path $Path
}


function Set-ACLManager {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $sysadminAce = New-ICEFullControl -Identifier "sysadmin"
    $chiefAce = New-ICEFullControl -Identifier "chief"
    $adminAce = New-ICEReadAndExecute -Identifier "admin"
    $managerRWXAce = New-ICEReadExecuteAndWriteContainer -Identifier "manager"
    $managerRXAce = New-ICEReadAndExecute -Identifier "manager"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)
    $targetAcl.AddAccessRule($adminAce)
    $targetAcl.AddAccessRule($managerRXAce)
    $targetAcl.AddAccessRule($managerRWXAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLAdmin {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $sysadminAce = New-ICEFullControl -Identifier "sysadmin"
    $chiefAce = New-ICEFullControl -Identifier "chief"
    $adminRWXAce = New-ICEReadExecuteAndWriteContainer -Identifier "admin"
    $adminRXAce = New-ICEReadAndExecute -Identifier "admin"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)
    $targetAcl.AddAccessRule($adminRXAce)
    $targetAcl.AddAccessRule($adminRWXAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLChief {
    param (
        [string]$Path
    )
    $targetAcl = Get-ACLDefault -Path $Path

    $sysadminAce = New-ICEFullControl -Identifier "sysadmin"
    $chiefAce = New-ICEFullControl -Identifier "chief"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLShared {
    param (
        [string]$Path
    )

    $originalAcl = Get-Acl -Path $Path
    $targetAcl = Get-Acl -Path $Path
    
    $targetAcl.SetAccessRuleProtection($true, $false)

    $employeeAce = New-ICEFullControl -Identifier "employee"
    $targetAcl.AddAccessRule($employeeAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLSpecial {
    param (
        [string]$Path,
        [string[]]$Identifiers
    )

    $originalAcl = Get-Acl -Path $Path
    $targetAcl = Get-Acl -Path $Path
    
    $targetAcl.SetAccessRuleProtection($true, $false)

    $sysadminAce = New-ICEFullControl  -Identifier "sysadmin"
    $chiefAce = New-ICEReadAndExecute  -Identifier "chief"

    foreach($identifier in $Identifiers) {
        $ace = New-ICEFullControl -Identifier $identifier
        $targetAcl.AddAccessRule($ace)
    }

    $targetAcl | Set-Acl -Path $Path
}
#endregion ACL

#region Directories
function New-ITSMDirectory {
    param (
        [string]$Path
    )

    New-Item -Path $Path -ItemType "Directory" | Out-Null
}
#endregion Directories

Remove-Item -Path "C:\Company\Chief"
Remove-Item -Path "C:\Company\Admin"
Remove-Item -Path "C:\Company\Manager"
Remove-Item -Path "C:\Company\Shared"
Remove-Item -Path "C:\Company\Special"
Remove-Item -Path "C:\Company"

Remove-LocalUser -Name "sysadmin1"
Remove-LocalUser -Name "chief1"
Remove-LocalUser -Name "admin1"
Remove-LocalUser -Name "admin2"
Remove-LocalUser -Name "manager1"
Remove-LocalUser -Name "manager2"
Remove-LocalUser -Name "manager3"
Remove-LocalUser -Name "manager4"
Remove-LocalUser -Name "supreme"

Remove-LocalGroup -Name "sysadmin"
Remove-LocalGroup -Name "chief"
Remove-LocalGroup -Name "admin"
Remove-LocalGroup -Name "manager"
Remove-LocalGroup -Name "employee"

New-ITSMLocalGroup -Name "sysadmin" 
New-ITSMLocalGroup -Name "chief" 
New-ITSMLocalGroup -Name "admin" 
New-ITSMLocalGroup -Name "manager"
New-ITSMLocalGroup -Name "employee"

New-ITSMLocalUser -Name "sysadmin1" -Groups "Administrators","sysadmin","employee"
New-ITSMLocalUser -Name "chief1" -Groups "chief","employee"
New-ITSMLocalUser -Name "admin1" -Groups "admin","employee"
New-ITSMLocalUser -Name "admin2" -Groups "admin","employee"
New-ITSMLocalUser -Name "manager1" -Groups "manager","employee"
New-ITSMLocalUser -Name "manager2" -Groups "manager","employee"
New-ITSMLocalUser -Name "manager3" -Groups "manager","employee"
New-ITSMLocalUser -Name "manager4" -Groups "manager","employee"
New-ITSMLocalUser -Name "supreme" -Groups "employee"

New-ITSMDirectory -Path "C:\Company"
Set-ACLRoot -Path "C:\Company"

New-ITSMDirectory -Path "C:\Company\Chief"
Set-ACLChief -Path "C:\Company\Chief"

New-ITSMDirectory -Path "C:\Company\Admin"
Set-ACLAdmin -Path "C:\Company\Admin"

New-ITSMDirectory -Path "C:\Company\Manager"
Set-ACLManager -Path "C:\Company\Manager"

New-ITSMDirectory -Path "C:\Company\Shared"
Set-ACLShared -Path "C:\Company\Shared"

New-ITSMDirectory -Path "C:\Company\Special"
Set-ACLSpecial -Path "C:\Company\Special" -Identifiers "admin2","manager3"