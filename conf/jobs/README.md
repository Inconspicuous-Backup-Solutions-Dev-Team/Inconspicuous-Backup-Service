# Directory "./conf/jobs/"

In this directory you create a ".json" file for each backup job you will run.
A backup job simply is a file that says:
"Write the backup from this host to this backup storage."

**Hint:**
All hosts are defined in "./conf/hosts/", all backup storages are defined
in "./conf/storages" storages.
      
The file names should follow the following naming convention:

<host file name>__to__<storage file name>

For example, a file name could look like this:

svn_example_com__to__mnt_backup_hdd1

As you might have noticed the files are in JSON format. You 'll find information
about the format itself on: https://en.wikipedia.org/wiki/JSON

The content of a file might look like this:
```javascript
{
    "description" : "Full backup of all servers to hard-disk /mnt/hdd1",
    "host" : "svn_example_com",
    "storage" : "mnt_backup_hdd1"
}
```
Each file contains a dictionary with the fields:
"description", "host", "storage"

The field "description" should contain a human readable description what the job
is all about. It's used for reporting and to make administration a little bit
easyer.

The field "host" contains the name of a configuration file found in
"./conf/hosts/" without the extension ".json".

The field "storage" names one of the files found in "./conf/storages"
without its extension ".json".
