
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

#region ACE

function New-ACEFullControl {
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

function New-ACEReadAndExecute {
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

function New-ACEReadExecuteAndWrite {
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

function New-ACESimpleReadAndWrite {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        ([FileSystemRights]::ReadData + [FileSystemRights]::WriteData), 
        ([InheritanceFlags]::ContainerInherit + [InheritanceFlags]::ObjectInherit), 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ACESimpleReadWriteAndAppend {
    param (
        [string]$Identifier
    )

    return New-Object FileSystemAccessRule(
        $Identifier, 
        ([FileSystemRights]::ReadData + [FileSystemRights]::WriteData + [FileSystemRights]::AppendData), 
        ([InheritanceFlags]::ContainerInherit + [InheritanceFlags]::ObjectInherit), 
        [PropagationFlags]::None, 
        [AccessControlType]::Allow)
}

function New-ACEFullControlContainer {
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

function New-ACEReadExecuteAndWriteContainer {
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

function New-ACEReadAndExecuteContainer {
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

#endregion ACE

#region ACL
function Get-ACLDefault {
    param (
        [string]$Path
    )

    $targetAcl = Get-Acl -Path $Path

    $targetAcl.SetAccessRuleProtection($true, $false)

    $creatorSystemAce = New-ACEFullControl -Identifier "NT AUTHORITY\SYSTEM"
    $creatorAdministratorsAce = New-ACEFullControl -Identifier "BUILTIN\Administrators"
    $creatorOwnerAce = New-ACEFullControl -Identifier "CREATOR OWNER"

    $targetAcl.AddAccessRule($creatorSystemAce)
    $targetAcl.AddAccessRule($creatorAdministratorsAce)
    $targetAcl.AddAccessRule($creatorOwnerAce)

    return $targetAcl
}

function Set-ACLRoot {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"
    $employeeAce = New-ACEReadAndExecuteContainer -Identifier "employee"

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

    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"
    $adminAce = New-ACEReadAndExecute -Identifier "admin"
    $managerRWXAce = New-ACEReadExecuteAndWriteContainer -Identifier "manager"
    $managerRXAce = New-ACEReadAndExecute -Identifier "manager"

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

    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"
    $adminRWXAce = New-ACEReadExecuteAndWriteContainer -Identifier "admin"
    $adminRXAce = New-ACEReadAndExecute -Identifier "admin"

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

    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLShared {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path
    
    $targetAcl.SetAccessRuleProtection($true, $false)

    $employeeAce = New-ACEFullControl -Identifier "employee"
    $targetAcl.AddAccessRule($employeeAce)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLSpecial {
    param (
        [string]$Path,
        [string[]]$Identifiers
    )

    $targetAcl = Get-ACLDefault -Path $Path
    
    $targetAcl.SetAccessRuleProtection($true, $false)

    $sysadminAce = New-ACEFullControl  -Identifier "sysadmin"
    $chiefAce = New-ACEReadAndExecute  -Identifier "chief"

    foreach($identifier in $Identifiers) {
        $ace = New-ACEFullControl -Identifier $identifier
        $targetAcl.AddAccessRule($ace)
    }

    $targetAcl | Set-Acl -Path $Path
}


function Set-ACLSupreme1 {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $srw = New-ACESimpleReadAndWrite -Identifier "supreme1"

    $targetAcl.AddAccessRule($srw)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLSupreme2 {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $srwa = New-ACESimpleReadWriteAndAppend -Identifier "supreme2"

    $targetAcl.AddAccessRule($srwa)

    $targetAcl | Set-Acl -Path $Path
}

function Set-ACLManagerAdmin {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    $rwx = New-ACEReadExecuteAndWrite -Identifier "admin2"

    $targetAcl.AddAccessRule($rwx)

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

#region Policies
function Export-SecurityPolicy {
    param (
        [string]$Path
    )
    secedit /export /cfg $Path | Out-Null
}

function Apply-SecurityPolicy {
    param (
        [string]$Path
    )
    secedit /configure /db c:\windows\security\local.sdb /cfg $Path /areas SECURITYPOLICY | Out-Null
}

function Set-SecurityPolicy {
    param (
        [string]$Policy,
        [string]$Value
    )

    $configPath = "C:\Temp\SecurityPolicy.cfg"
    Export-SecurityPolicy -Path $configPath
    
    [regex]$regex = [string]::format("(?m)^{0}.*$", $Policy)
    $replacement = [string]::format("{0} = {1}", $Policy, $Value)

    (Get-Content $configPath -Raw) -replace $regex,$replacement | Out-File $configPath

    Apply-SecurityPolicy $configPath

    Remove-Item -Path $configPath -Force -Confirm:$False
}

function Configure-SecurityPolicy {
    Export-SecurityPolicy -Path "C:\Temp\DefaultSecurityPolicy.cfg"
    Set-SecurityPolicy -Policy "PasswordComplexity" -Value "1"
    Set-SecurityPolicy -Policy "MinimumPasswordLength" -Value "12"
    Set-SecurityPolicy -Policy "MaximumPasswordAge" -Value "60"
    Set-SecurityPolicy -Policy "PasswordHistorySize" -Value "5"
    Set-SecurityPolicy -Policy "AuditSystemEvents" -Value "3"
    Set-SecurityPolicy -Policy "AuditLogonEvents" -Value "3"
    Set-SecurityPolicy -Policy "AuditObjectAccess" -Value "3"
    Set-SecurityPolicy -Policy "AuditPrivilegeUse" -Value "3"
    Set-SecurityPolicy -Policy "AuditPolicyChange" -Value "3"
    Set-SecurityPolicy -Policy "AuditAccountManage" -Value "3"
    Set-SecurityPolicy -Policy "AuditProcessTracking" -Value "3"
    Set-SecurityPolicy -Policy "AuditDSAccess" -Value "3"
    Set-SecurityPolicy -Policy "AuditAccountLogon" -Value "3"
}

function Configure-GroupPolicy {
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Force -Type "DWord" -Name "NoDispCPL" -Value 1
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Force -Type "DWord" -Name "NoChangingWallpaper" -Value 1
    Set-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\RemovableStorageDevices" -Force -Type "DWord" -Name "Deny_All" -Value 1
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Force -Type "DWord" -Name "HidePowerOptions" -Value 1
}

function Restore-GroupPolicy {
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "NoDispCPL"
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "NoChangingWallpaper"
    Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\RemovableStorageDevices" -Name "Deny_All"
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "HidePowerOptions"
}


function Restore-SecurityPolicy {
    New-ITSMDirectory -Path "C:\Temp" 2>&1 | Out-Null
    Apply-SecurityPolicy -Path "C:\Temp\DefaultSecurityPolicy.cfg"
}
#endregion Policies

#region State
function Restore-Machine {
    Restore-GroupPolicy
    Restore-SecurityPolicy

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
    Remove-LocalUser -Name "supreme1"
    Remove-LocalUser -Name "supreme2"

    Remove-LocalGroup -Name "sysadmin"
    Remove-LocalGroup -Name "chief"
    Remove-LocalGroup -Name "admin"
    Remove-LocalGroup -Name "manager"
    Remove-LocalGroup -Name "employee"
}

function Configure-Machine {
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
    New-ITSMLocalUser -Name "supreme1" -Groups "employee"
    New-ITSMLocalUser -Name "supreme2" -Groups "employee"

    New-ITSMDirectory -Path "C:\Company"
    Set-ACLRoot -Path "C:\Company"

    New-ITSMDirectory -Path "C:\Company\Chief"
    Set-ACLChief -Path "C:\Company\Chief"

    New-ITSMDirectory -Path "C:\Company\Admin"
    Set-ACLAdmin -Path "C:\Company\Admin"
    Set-ACLSupreme1 -Path "C:\Company\Admin"

    New-ITSMDirectory -Path "C:\Company\Manager"
    Set-ACLManager -Path "C:\Company\Manager"
    Set-ACLSupreme2 -Path "C:\Company\Manager"
    Set-ACLManagerAdmin -Path "C:\Company\Manager"

    New-ITSMDirectory -Path "C:\Company\Shared"
    Set-ACLShared -Path "C:\Company\Shared"

    New-ITSMDirectory -Path "C:\Company\Special"
    Set-ACLSpecial -Path "C:\Company\Special" -Identifiers "admin2","manager3"

    Configure-SecurityPolicy
    Configure-GroupPolicy
}

#endregion State

Restore-Machine
Configure-Machine

# Crashing 
# https://stackoverflow.com/questions/4284913/force-crash-an-application
# windbg -pn notepad.exe
# 0:008> ~0s 
# 0:000> rip=0
# 0:000> qd