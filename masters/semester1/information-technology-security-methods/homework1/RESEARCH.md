# Research

## Task 9

We have to use all the tools that are specified in the task.

> Windows: icacls, takeown, inheritance, net accounts, LGP (local group policy),
auditpol, NTRIGHTS

> Linux: chmod, setfacl, getfacl, default ACL, SUID, GUID, sticky bit, chown,
passwd, chattr

### Linux Tools

#### Basic permissions (rwx)

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

#### Displaying permissions
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

#### chmod

This command changes the basic permissions (rwx) for a file.

```
      uga
chmod 777 /path/to/file

4 - read 
2 - write
1 - execute
```

#### SUID

SUID (Set owner User ID) is a permission bit that can be set on an executable file or [directory](https://www.gnu.org/software/coreutils/manual/html_node/Directory-Setuid-and-Setgid.html).

When set, the permission shows an `s` symbol for `owner execute permission`:
```
   ↓
-rwsrwxr-x
```

If set on a file, when the file is executed, it will be executed with the same permissions as the owner of the file. 

For example, `/usr/bin/passwd` has SUID set, and as such, regular users are able to use it to change their own password (even if the files being modified can only be modified by root).

```
ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 kov.   14  2022 /usr/bin/passwd

ls -l /etc/passwd
-rw-r--r-- 1 root root 3169 birž.  29 19:16 /etc/passwd
```

To set/unset the SUID one would run the following:
```
# set SUID
chmod u+s file_name

# unset SUID
chmod u-s file_name
```

If the file has a capital `S` as the bit, it means that the SUID bit is set, but `x` permission is not set. In this state, SUID has no use, as the file cannot be executed.







