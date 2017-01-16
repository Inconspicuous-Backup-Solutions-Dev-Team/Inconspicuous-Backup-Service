# Inconspicuous Backup Service

This software backs up data over network from Linux and Unix-like servers and
workstations. It's meant to run on a dedicated backup server. The machines which
are backed up will be called "hosts" in the rest of this document.

Each host is accessed by the backup server via SSH. The backup server copies
all files that need to be backed up from a configured host to the first level
backup directory.

This copy is backed up to backup storages as they are configured. Which
host's copy of data is backed up to which storage is defined in a job definition.

When each job will run is defined via symbolic links in the schedule
configuration directories.

## Basic Configuration:

You don't have to install any specific software on the clients themselves.
However, you have to enable the root user of the backup server to access all
clients via SSH without using a password. How to use certificates instead of
passwords for SSH is well documented. For example enter these words into your
favourite internet search engine: "ssh passwordless login" or take a look at
the provided file “HOWTO_INSTALL_SSH.md”.

After granting the root of your backup server access to all other servers, you
have to configure the backup software. (Keep in mind your backup server is very
powerful now. It should run no network server processes and should be very well
hardened.)

For main configuration you edit the file "configuration.json", which should
look like this:

```javascript
{
  "first_level_backup_directory": "/mnt/first_level_backup_storage",
  "report_directory": "/mnt/webserver/www/htdocs/backup_reports",
  "email": {
    "server": "mail.example.com:25",
    "username": "backup@example.com",
    "password": "Some$avePassword",
    "from": "backup@example.com",
    "to": [ "admin@example.com" ]
  }
}
```

As you might have noticed the files are in JSON format. You'll find information
about the format itself on: https://en.wikipedia.org/wiki/JSON

Each file contains a dictionary with the fields:
"first_level_backup_directory", "report_directory", "email"

The Field "first_level_backup_directory" is the path to a directory where all
data from all hosts gets mirrored to before writing it to the final backup.

The Field "report_directory" is a directory where a report gets stored each
time the backup actually runs. The report will be an HTML file.

The Field "email" contains a configuration for email notifications. Each time
the backup actually runs an email is sent to report success or failure.

## Hosts

After general configuration of SSH and the basic configuration, host
configurations are the next important thing to create.

All host configuration files will live quite happily in the directory
"./conf/hosts". Within this directory you will find another "README.md" file
that explains the content of host configuration files in detail.

To wrap up, a host configuration file defines a host and which of its
data needs to be backed up.

When you are done with all configuration steps for integrating the hosts, you
should run the backup script in test mode. It will ensure that everything is
working as expected so far.

## Storages

Having done the preparations and the basic configuration and having defined
where the data comes from, it's time to write down where the backups will be
stored.
This task is done by the configuration files in "./conf/storages". Within this
directory you’ll find another "README.md" file, that explains the content of
storage configuration files in detail.

In short, each storage configuration file represents a storage target
e.g. a hard-disk or a tape. It also defines the backup strategy (like
incremental or full copy) that is used to write data to it.

## Jobs

Basic set-up is done. You have your hosts where the data is coming from. You
have your storages where the backups are written to. Time to tie it all
together.
To do so you create jobs. Job configuration files can to be found in
"./conf/jobs". Within this directory you will find another "README.md" file,
that explains the content of job configuration files in detail.
To sum it up a job simply says: "Write the backup from this host to this
backup storage."

## Schedule

Basic set-up is done. You have your data sources (hosts), your backup media
(storages) and the glue in between (jobs). Now it's time for scheduling.
There is a Cron configuration file you can apply to the "crontab" of your backup
server.
Corresponding to the Cron configuration file, you have the directory
"./conf/schedule". In the schedule directory there is a subdirectory for each
time the backup will run. If you want a job to run at one of those times,
you simply put a symbolic link to the job file into that directory.

Let's assume you installed the backup program in "/opt/backup" and you have
created a job file "all_servers_to_mnt_backup_hdd1.json" you want to run
at the end of every weekday (Mo-Fr). Then you create your symbolic link like
this:

```bash
ln -s /opt/backup/jobs/all_servers_to_mnt_backup_hdd1.json \
 /opt/backup/schedule/end_of_every_weekday/all_servers_to_mnt_backup_hdd1.json
```
