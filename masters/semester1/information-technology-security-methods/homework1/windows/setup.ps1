
using namespace System.Security.AccessControl;

#region Identities

# Command that creates a new user.
# The user is added to the builtin `Users` group, as well as any
# groups that are specified in the $Groups parameter.
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

# Command that creates a new group.
function New-ITSMLocalGroup {
    param (
        [string]$Name
    )

    New-LocalGroup -Name $Name | Out-Null
}
#endregion Identities

#region ACE

# ACE - Access Control Entry
# Commands within this region creates specified ACEs for ease of use.
# Commands with `Container` at the end creates ACEs that only has inheritance for folders/subfolders.

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

# Commands within this region uses the commands from ACE region
# to create full ACL for specific folders or use cases.


# This command removes ACL inheritance and removes existing
# ACE from ACL.
function Clear-ACL {
    param (
        [string]$Path
    )

    $targetAcl = Get-Acl -Path $Path

    $targetAcl.SetAccessRuleProtection($true, $false)
   
    $targetAcl | Set-Acl -Path $Path
}

# This command creates default ACL for use between all folders
function Get-ACLDefault {
    param (
        [string]$Path
    )

    $targetAcl = Get-Acl -Path $Path

    # System, Administrators and file owner should have full access to created files
    $creatorSystemAce = New-ACEFullControl -Identifier "NT AUTHORITY\SYSTEM"
    $creatorAdministratorsAce = New-ACEFullControl -Identifier "BUILTIN\Administrators"
    $creatorOwnerAce = New-ACEFullControl -Identifier "CREATOR OWNER"

    $targetAcl.AddAccessRule($creatorSystemAce)
    $targetAcl.AddAccessRule($creatorAdministratorsAce)
    $targetAcl.AddAccessRule($creatorOwnerAce)

    return $targetAcl
}

# ACL for the main, root folder.
function Set-ACLRoot {
    param (
        [string]$Path
    )

    # Usage of the default ACL.
    $targetAcl = Get-ACLDefault -Path $Path

    # Sysadmin and Chief has full access, while employees can only read and execute on directories.
    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"
    $employeeAce = New-ACEReadAndExecuteContainer -Identifier "employee"

    $targetAcl.AddAccessRule($sysadminAce)
    $targetAcl.AddAccessRule($chiefAce)
    $targetAcl.AddAccessRule($employeeAce)

    $targetAcl | Set-Acl -Path $Path
}

# Sets owner of specified path
function Set-ACLOwner {
    param (
        [string]$Path,
        [string]$Owner
    )

    $owner = Get-LocalUser -Name $Owner 
    $targetAcl = Get-ACLDefault -Path $Path

    $targetAcl.SetOwner($owner)

    $targetAcl | Set-Acl -Path $Path
}


function Set-ACLManager {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    # Sysadmin and chief has full access to the folder, admin have
    # read and execute access.
    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"
    $adminAce = New-ACEReadAndExecute -Identifier "admin"

    # Managers have read, write and execute on current directory, and child directories.
    # They only have read and execute on all other files.
    # This means, that only the owner of the files can modify them.
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

    # Sysadmin and chief has full access to the folder, admin have
    # read and execute access.
    $sysadminAce = New-ACEFullControl -Identifier "sysadmin"
    $chiefAce = New-ACEFullControl -Identifier "chief"

    # Admins have read, write and execute on current directory, and child directories.
    # They only have read and execute on all other files.
    # This means, that only the owner of the files can modify them.
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

    # Sysadmin and chief has full access to the folder, admin have
    # read and execute access.
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

    # Employees have full access on files and folders within this folder
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

    # Sysadmin has full access, while chief has only read access on the special folder
    # and specified $Identifiers have full access to the folder as well.
    $sysadminAce = New-ACEFullControl  -Identifier "sysadmin"
    $chiefAce = New-ACEReadAndExecute  -Identifier "chief"

    foreach($identifier in $Identifiers) {
        $ace = New-ACEFullControl -Identifier $identifier
        $targetAcl.AddAccessRule($ace)
    }

    $targetAcl | Set-Acl -Path $Path
}

# Special ACL for Supreme1 user
function Set-ACLSupreme1 {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    # Special ACE for Supreme1 user, which only allows reading and writing data.
    # Appending data, or editing of metadata is not permitted.
    $srw = New-ACESimpleReadAndWrite -Identifier "supreme1"

    $targetAcl.AddAccessRule($srw)

    $targetAcl | Set-Acl -Path $Path
}

# Special ACL for Supreme2 user
function Set-ACLSupreme2 {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    # Special ACE for Supreme2 user, which only allows reading, writing and appending data.
    # Editing of metadata is not permitted.
    $srwa = New-ACESimpleReadWriteAndAppend -Identifier "supreme2"

    $targetAcl.AddAccessRule($srwa)

    $targetAcl | Set-Acl -Path $Path
}

# Special ACL for admin2 user
function Set-ACLAdmin2 {
    param (
        [string]$Path
    )

    $targetAcl = Get-ACLDefault -Path $Path

    # ACE permitting read, write and execute on a folder for admin2 user
    $rwx = New-ACEReadExecuteAndWrite -Identifier "admin2"

    $targetAcl.AddAccessRule($rwx)

    $targetAcl | Set-Acl -Path $Path
}

#endregion ACL

#region Directories

# Helper command for creating directory directly.
function New-ITSMDirectory {
    param (
        [string]$Path
    )

    New-Item -Path $Path -ItemType "Directory" | Out-Null
}
#endregion Directories

#region Policies

# Commands within this region assist with modification of security policies.

# The following command is a wrapper for a `secedit` executable for exporting Security Policy.
function Export-SecurityPolicy {
    param (
        [string]$Path
    )
    secedit /export /cfg $Path | Out-Null
}

# The following command is a wrapper for a `secedit` executable for applying modified Security Policy.
function Apply-SecurityPolicy {
    param (
        [string]$Path
    )
    secedit /configure /db c:\windows\security\local.sdb /cfg $Path /areas SECURITYPOLICY | Out-Null
}

# Command helper that allows modyfing a policy.
function Set-SecurityPolicy {
    param (
        [string]$Policy,
        [string]$Value
    )

    # 1. Exporting the policy configuration file
    $configPath = "C:\Temp\SecurityPolicy.cfg"
    Export-SecurityPolicy -Path $configPath
    
    # 2. Preparing regex match statement and replacement
    [regex]$regex = [string]::format("(?m)^{0}.*$", $Policy)
    $replacement = [string]::format("{0} = {1}", $Policy, $Value)

    # 3. Replacing the lines in the configuration file
    (Get-Content $configPath -Raw) -replace $regex,$replacement | Out-File $configPath

    # 4. Applying the policy configuration
    Apply-SecurityPolicy $configPath

    # 5. Removing the temporary file
    Remove-Item -Path $configPath -Force -Confirm:$False
}

# Function that configures the entire Security Policy.

function Configure-SecurityPolicy {
    # We export default security policy, so that we could revert the changes, if needed.
    Export-SecurityPolicy -Path "C:\Temp\DefaultSecurityPolicy.cfg"
    
    # Password policy changes
    Set-SecurityPolicy -Policy "PasswordComplexity" -Value "1"
    Set-SecurityPolicy -Policy "MinimumPasswordLength" -Value "12"
    Set-SecurityPolicy -Policy "MaximumPasswordAge" -Value "60"
    Set-SecurityPolicy -Policy "PasswordHistorySize" -Value "5"

    # Enabling of audit event logging
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

# Group policy configuration function
function Configure-GroupPolicy {

    # Works by modifying registry entries directly.

    # Prevents editing of display configuration
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Force -Type "DWord" -Name "NoDispCPL" -Value 1

    # Prevents editing of background wallpaper
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Force -Type "DWord" -Name "NoChangingWallpaper" -Value 1

    # Denies access to ALL classes of removable storage media
    Set-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\RemovableStorageDevices" -Force -Type "DWord" -Name "Deny_All" -Value 1

    # Disables powerbuttons for users, in Start, Ctrl+Alt+Del menus etc. Still allows system to be powered off with enough commands and shutdown command.
    Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Force -Type "DWord" -Name "HidePowerOptions" -Value 1
}

function Restore-GroupPolicy {
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "NoDispCPL"
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "NoChangingWallpaper"
    Remove-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\RemovableStorageDevices" -Name "Deny_All"
    Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "HidePowerOptions"
}

# Restores Security Policy by reverting 
function Restore-SecurityPolicy {
    New-ITSMDirectory -Path "C:\Temp" 2>&1 | Out-Null
    Apply-SecurityPolicy -Path "C:\Temp\DefaultSecurityPolicy.cfg"
}
#endregion Policies

#region State

# The following functions aggregate all the functions above, to restore or apply the wanted state of the system.
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

    # Task 1 is completed here.

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
    Clear-ACL -Path "C:\Company"
    Set-ACLRoot -Path "C:\Company"

    New-ITSMDirectory -Path "C:\Company\Chief"
    Clear-ACL -Path "C:\Company\Chief"
    Set-ACLChief -Path "C:\Company\Chief"
    # Completion of Task 2. Provide write rights to admin2, for a Chief folder.
    Set-ACLAdmin2 -Path "C:\Company\Chief" 

    New-ITSMDirectory -Path "C:\Company\Admin"
    Clear-ACL -Path "C:\Company\Admin"
    Set-ACLAdmin -Path "C:\Company\Admin"
    Set-ACLSupreme1 -Path "C:\Company\Admin"

    New-ITSMDirectory -Path "C:\Company\Manager"
    Clear-ACL -Path "C:\Company\Manager"
    Set-ACLManager -Path "C:\Company\Manager"
    # Additional task 2 is completed, by addition of additional users
    # with special permissions.
    Set-ACLSupreme2 -Path "C:\Company\Manager" 

    New-ITSMDirectory -Path "C:\Company\Shared"
    Clear-ACL -Path "C:\Company\Shared"
    Set-ACLShared -Path "C:\Company\Shared"

    New-ITSMDirectory -Path "C:\Company\Special"
    Clear-ACL -Path "C:\Company\Special"
    Set-ACLSpecial -Path "C:\Company\Special" -Identifiers "admin2","manager3"

    # Completion of Task 6
    Set-ACLOwner -Path "C:\Company\Special" -Owner "admin2"
    Set-ACLOwner -Path "C:\Company\Manager" -Owner "manager1"

    # Completion of Task 3, 5 and 8. By configuring the security policy,
    # we update the password policy and enable audit logging for required events.
    Configure-SecurityPolicy

    # Completion of task 4. By configuring group policy/registry keys, we
    # prevent use of specified functionality.
    Configure-GroupPolicy

    # Additional task 1 is completed by use of PowerShell
}

#endregion State

Restore-Machine
Configure-Machine

# Completion of additional task 3 is done here, although it does require a live demonstration.

# Crashing 
# https://stackoverflow.com/questions/4284913/force-crash-an-application
# windbg -pn notepad.exe
# 0:008> ~0s 
# 0:000> rip=0
# 0:000> qd