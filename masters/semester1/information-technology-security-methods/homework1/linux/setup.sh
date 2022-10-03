#!/usr/bin/bash

# Creates a group with the specified name
create_group () {
  local groupname=$1
  echo "Adding group \"$groupname\""
  groupadd $groupname
}

delete_group () {
  local groupname=$1
  echo "Adding group \"$groupname\""
  delgroup $groupname
}

# Creates a user in specified groups and expires the
# default password immediately.
create_user () {
  local username=$1
  local group=$2
  local aux_groups=$3
  local home_dir=$4
  echo "Adding user \"$username\" ($group,$aux_groups) $home_dir"
  useradd -d $home_dir -g $group -G $aux_groups -N -M --shell /usr/bin/bash $username
  # the following line expires user password immediately sets maximum password age to 90 days 
  # it is disabled to make running of the script a bit easier
  #passwd -d -e -x 90 $username 
  passwd -d $username
}

delete_user () {
  local username=$1
  deluser --force $username
}

create_dir () {
  local dir=$1
  local permissions=${2//,/$'\n'}
  echo "Creating directory \"$dir\" with \"$2\" permissions."
  mkdir -p $dir
  for permission in $permissions; do
    setfacl -M $permission $dir
  done
}

delete_dir () {
  local dir=$1
  rm -rf $dir
}

set_acl () {
  local filename=$1
  local permissions=${2//,/$'\n'}
  echo "Setting file \"$filename\" permissions to \"$2\"."
  for permission in $permissions; do
    setfacl -M $permission $filename
  done
}

create_file () {
  local filename=$1
  local permissions=$2
  echo "Creating file \"$filename\"."
  echo $filename > $filename
  set_acl $filename $permissions
}

run_as () {
  local user=$1
  local command=$2
  su $user -c "$command"
}

# Reset state

cp common-password.default /etc/pam.d/common-password
cp audit.rules.default /etc/audit/audit.rules

delete_user sysadmin     
delete_user chief    
delete_user admin1    
delete_user admin2    
delete_user manager1    
delete_user manager2    
delete_user manager3    
delete_user manager4    
delete_user supreme 

delete_group sysadmin
delete_group chief
delete_group admin
delete_group manager
delete_group supreme
delete_group employee

delete_dir /company

# Begin script

# Create groups (task 1)
create_group sysadmin
create_group chief
create_group admin
create_group manager
create_group supreme
create_group employee

# Create users (task 1)
create_user sysadmin     sysadmin employee /company
create_user chief        chief    employee /company/chief
create_user admin1       admin    employee /company/admin
create_user admin2       admin    employee /company/admin
create_user manager1     manager  employee /company/manager
create_user manager2     manager  employee /company/manager
create_user manager3     manager  employee /company/manager
create_user manager4     manager  employee /company/manager
create_user supreme      supreme  employee /company

# Create directories with specified permissions (task 1)
create_dir  /company                     0.default,1.sysadmin,5.employee
create_dir  /company/chief               0.default,2.chief
create_dir  /company/admin               0.default,3.admin,0.supreme_dir
create_dir  /company/manager             0.default,4.manager
create_dir  /company/shared              0.default,0.shared
create_dir  /company/special             0.default,0.special
create_file /company/admin/admin_secrets 0.supreme_file

# Enable better password policy (task 3)
cp common-password.best /etc/pam.d/common-password
# Enable better auditing (task 5, 8)
cp audit.rules.best /etc/audit/audit.rules

# Providing write permissions for a management user to a chief directory (task 2)
setfacl -m user:manager4:-w- /company/chief

# Preventing use of a terminal and network interface configuration (task 4)
set_acl /usr/bin/gnome-terminal.real 0.disable
set_acl /usr/bin/gnome-terminal 0.disable
set_acl /usr/bin/ip 0.disable
set_acl /usr/sbin/ip 0.disable

# Creating a file via user and administrator accounts, and taking ownership (task 6)
run_as admin1 "touch /company/shared/admin1_file"
run_as manager1 "touch /company/shared/manager1_file"
chown sysadmin:sysadmin /company/shared/admin1_file
chown sysadmin:sysadmin /company/shared/manager1_file
