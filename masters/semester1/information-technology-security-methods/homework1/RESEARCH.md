# Research

## Task 3

Suggested tools for managing assword policy.

> Windows: local security policy, #net accounts

> Linux: **PAM**, **chage**

## Task 9

We have to use all the tools that are specified in the task.

> Windows: icacls, takeown, inheritance, net accounts, LGP (local group policy),auditpol, NTRIGHTS

> Linux: **chmod**, **setfacl**, **getfacl**, **default ACL**, **SUID**, **GUID**, **sticky bit**, **chown**, **passwd**, chattr



## Linux Tools

### Sources

`man`

[Linux Handbook - SUID, SGID, Sticky Bit](https://linuxhandbook.com/suid-sgid-sticky-bit/)

[Why can't a normal user chown a file](https://unix.stackexchange.com/questions/27350/why-cant-a-normal-user-chown-a-file/27374#27374)

[FreeBSD - Pluggable Authentication Modules](https://docs.freebsd.org/en/articles/pam/)

[knobs-dials.com - PAM notes](https://helpful.knobs-dials.com/index.php/PAM_notes)

[How To Set Password Policies In Linux](https://ostechnix.com/how-to-set-password-policies-in-linux/)

[An introduction to Linux Access Control Lists (ACLs)](https://www.redhat.com/sysadmin/linux-access-control-lists)

### Basic permissions (rwx)

Files and directories can have these kinds of *basic* permissions:
* Read (r):
  * File: Read file contents
  * Directory: List directory contents
* Write (w):
  * File: Change file contents
  * Directory: Create/remove files within the directory
* Execute (x):
  * File: Execute the file
  * Directory: Access files within the directory

There permissions are granted for three types of categories of users:
* Owner (User | u)
* Group (Group | g)
* Others (All | a)

### Displaying permissions
The file/directory permissions are displayed (using `ls -la`) as follows:
```
Permissions Links Owner      Group      Size Modified        Name
-rwxrwxr-x  1     markcdavid markcdavid 1    lapkr. 15  2021 file
drwxrwxr-x  2     markcdavid markcdavid 1    lapkr. 15  2021 directory
```

The permissions indicate the following:
```
Directory Owner Group Others
d         rwx   rwx   r-x
```

### chmod

This command changes the basic permissions (rwx) for a file/directory.

```
      uga
chmod 777 /path/to/file

4 - read 
2 - write
1 - execute
```

### chown

This command changes the owner(:group) for a file/directory.

```
chown owner(:group) /path/to/file
```

`chown` command is a root-only utility, due to [certain security issues](https://unix.stackexchange.com/a/27374).

### passwd

A command that changes passwords for users. 

A regular user can only change their own password, a root user can change password of any account.

```
passwd user
```

`passwd` command has SUID set, which allows everyone to run the command with root permissions, as the command edits files that are owned by the root user.
```
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 kov.   14  2022 /usr/bin/passwd
   ↑
```

There are a few flags that might be important to the execution of the given scenario:

`-x, --maxdays MAX_DAYS` - sets how many days a password is valid for, until it **HAS** to be changed

`-e, --expire` - immediately expires the users password, forcing them to change the password on next login

### chage

A command that is capable of changing user password expiration dates. It uses some similar flags, to the command `passwd`.

`-M, --maxdays MAX_DAYS` - sets how many days a password is valid for, until it **HAS** to be changed

### SUID

SUID (Set owner User ID) is a permission bit that can be set on an executable file or [directory](https://www.gnu.org/software/coreutils/manual/html_node/Directory-Setuid-and-Setgid.html).

When set, the permission shows an `s` symbol for `owner user execute permission`:
```
   ↓
-rwsrwxr-x
```

#### SUID on a File

If set on a file, when the file is executed, it will be executed with the same permissions as the owner of the file. 

For example, `/usr/bin/passwd` has SUID set, and as such, regular users are able to use it to change their own password (even if the files being modified can only be modified by root).

```
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 kov.   14  2022 /usr/bin/passwd
   ↑

ls -l /etc/passwd
-rw-r--r-- 1 root root 3169 birž.  29 19:16 /etc/passwd
              ↑↑
```

To set/unset the SUID one would run the following:
```
# set SUID
chmod u+s file_name

# unset SUID
chmod u-s file_name

# octal number for SUID is 4
chmod 4777 file_name
```

If the file has a capital `S` as the bit, it means that the SUID bit is set, but `x` permission is not set. In this state, SUID has no use, as the file cannot be executed.

#### SUID on a Directory

While in some systems (according to the [GNU coreutils manual](https://www.gnu.org/software/coreutils/manual/html_node/Directory-Setuid-and-Setgid.html)), the SUID set on a directory might have some meaning, in Linux this bit has no meaning.

In Linux, regular users cannot give files away to other users ([source](https://unix.stackexchange.com/questions/27350/why-cant-a-normal-user-chown-a-file/27374#27374)), and as such SUID set on a directory follows suit, and files/directories created within a directory with SUID set, are still created with creator ownership.

### GUID/SGID

SGID (Set owner Group ID) is a permission bit that can be set on an executable file or directory.

When set, the permission shows an `s` symbol for `owner group execute permission`:
```
      ↓
-rwxrwsr-x
```

#### SGID on a File

Works very similarly to SUID, except elevates executing users privileges to that of the group owner.

#### SGID on a Directory

As opposed to SUID on a directory, SGID has a very practical use when set on a directory. 

When it is applied, any file created within the directory will have the owner group set to that, of the parent directory. When a directory is created, in addition to the owner group being set, it will have the SGID bit set as well.

This means, that the entire tree within a directory marked with SGID, will have SGID set. This makes it easier for a group of users to exchange files, as it reduces the need of using `chown` and `chgrp` commands respectivelly.

To set/unset the SGID one would run the following:
```
# set SGID
chmod g+s directory_name

# unset SGID
chmod g-s directory_name

# octal number for SUID is 2
chmod 2777 directory_name
```

If the directory has a capital `S` as the bit, it means that the SGID bit is set, but `x` permission is not set. In this state, SGID has no use, as no new files/directories can be created within the folder.

### Sticky Bit

Sticky bit is a permission bit that can be set on an executable file or directory.

When set, the permission shows an `t` symbol for `others execute permission`:
```
         ↓
-rwxrwxr-t
```

#### Sticky Bit on a file

Linux system ignores sticky bits on a file.

#### Sticky Bit on a Directory

When sticky bit is set on a directory, files within the directory can only be deleted by their owner or root user.

Usually, `/tmp` folder has this bit set, as multiple users/services can dump temporary files/directories without fear of other users removing that data.

```
ls -ld /tmp/
drwxrwxrwt 30 root root 40960 rugs.  16 22:58 /tmp/
         ↑
```

To set/unset the Sticky Bit one would run the following:
```
# set SGID
chmod +t directory_name

# unset SGID
chmod -t directory_name

# octal number for SUID is 1
chmod 1777 directory_name
```

### PAM / Pluggable Authentication Modules

A set of libraries that allows fine tuned configuration for user authentication.

#### Configuration files

PAM configuration files are usually stored in `/etc/pam.d` directory. A file within that directory corresponds to the application that is trying to authenticate. If the application that is trying to authenticate using PAM does not find a configuration file in the directory, it uses the default `/etc/pam.conf` file.

#### Policy Configuration 

Each policy configuration file contains rules using the following syntax:

```
Facility  Control Flag                    Module        Arguments
auth      [success=1 default=ignore]      pam_unix.so   nullok_secure
auth      requisite                       pam_deny.so
```

If policy configuration is done outside `/etc/pam.d`, an additional field must be set:

```
Application Facility  Control Flag                    Module        Arguments
sshd        auth      [success=1 default=ignore]      pam_unix.so   nullok_secure
```

#### Facilities

`auth` - Authentication and establishment of account credentials;

`account` - Access handling (e.g. account expiration, time-of-day);

`session` - Tasks associated with session set-up and tear-down.

`password` - Update of authentication token

#### Chains

A policy is made up of four chains, each for one of available facilities (`auth`, `account`, `session`, `password`).

A chain is a sequence of statements, specifying control flag, module and arguments. 

#### Control Flags

There exists five named control flags:

`binding`
* `SUCCESS` - If no prior failure occured, module immediately breaks and grants access. 
* `FAILURE` - Rest of the chain is executed, access will ultimately be denied.

`required` 
* `SUCCESS` - Rest of the chain is executed, will grant access (if no other failures occured)
* `FAILURE` - Rest of the chain is executed, access will ultimately be denied.

`requisite` 
* `SUCCESS` - Rest of the chain is executed, will grant access (if no other failures occured)
* `FAILURE` - Chain is immediately terminated, access is denied.

`sufficient` 
* `SUCCESS` - Chain is immediately terminated, will immediately grant access
* `FAILURE` - Module is ignored, rest of the chain is executed

`optional` 

Module is executed, but the results are ignored. 

**NOTE:** The request will be granted ***if and only if*** at least one module was executed and all non-optional modules has succeeded.

### ACL

Default Linux permissions are not extensive enough to support more complex access control scenarios. 

#### Viewing ACL

`getfactl <file>`

The format is as follows:

```
# file: somedir/                             ::: Name of the file
# owner: lisa                                ::: User owner of the file
# group: staff                               ::: Group owner of the file
# flags: -s-                                 ::: SUID, SGID, Sticky Bit flags
user::rwx                                    ::: Base ACL entry for user owner
user:joe:rwx               #effective:r-x    ::: Named user ACL entry for group owner
group::rwx                 #effective:r-x    ::: Base ACL entry for group owner - Linux permissions
group:cool:r-x                               ::: Named group ACL entry for group owner
mask::r-x                                    ::: Effective rights mask - provides effective rights masking for groups and named users
other::r-x                                   ::: Base ACL entry for user owner
default:user::rwx                            ::: Default user owner permissions, to be inherited
default:user:joe:rwx       #effective:r-x    ::: Default named user owner permissions, to be inherited
default:group::r-x                           ::: Default group owner permissions, to be inherited
default:mask::r-x                            ::: Default effective rights mask, to be inherited
default:other::---                           ::: Default permissions for other users, to be inherited
```

#### Modifying ACL

`setfacl [{-m|-x} ACL] file`

`setfacl [{-M|-X} ACL_FILE] file`

`--set`, `--set-file` flags are for ***replacing*** ACL

`-m`, `-M` flags are for modifying ACL (adding, editing)

`-x`, `-X` flags are for removing ACL

The `--set-file`, `-M` and `-X` flags are used to read ACL from files. The file must have ***at most*** one entry per line. `#` symbol symbolizes a comment, from start of the symbol, until end of the line.

`-d` flag is used to apply the `default` ACLs for inheritance. It's possible to set defaults without usage of the flag.


#### ACL Format
Permissions for a user: `[default:] [user:]uid [:permissions]`.
***uid*** can be empty. If so, permissions are aplied for user owner. 

Permissions for a group: `[default:] group:uid [:permissions]`
***uid*** can be empty. If so, permissions are aplied for group owner. 

Effective rights mask: `[default:] mask [:permissions]`

Permissions for others: `[default:] other [:permissions]`

Examples:
```
default:user:markcdavid:rw- # Default ACL for named user 'markcdavid', with rw permissions
user::rwx # ACL for user owner, with rwx permissions
mask:r-x # ACL Effective rights mask, with rw permissions
```

