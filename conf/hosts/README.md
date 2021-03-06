# Directory "./conf/hosts/"

In this directory you create a ".json" file for each host you want to backup.

The name of the file will be used as the name of the backup directory
crated for the host. It's recommended to name the files similar to the
fully qualified name of the host or it's IP address if you don't use names:

* myserver.mydomain.com => myserver_mydomain_com.json
* somehost.exammple.com => somehost_example_com.json
* 192.168.1.23          => 192_168_1_23

The content of such a file could look like this:
```javascript
{
  "host": "somehost.example.com",
  "services": {
    "mysql": { "username": "root", "password": "SecrectPassword" },
    "postgresql": { "username": "postgres" },
    "subversion": { "repositories_directory": "/var/lib/svn" }
  },
  "directories": [ "/home", "/var/documents" ]
}
```
Or it can look like this other example:
```javascript
{
  "host": "192.168.1.23",
  "services": { },
  "directories": [ "/var/svn" ]
}
```
As you might have noticed, the files are in JSON format. You 'll find
information about the format itself on: https://en.wikipedia.org/wiki/JSON

Each file contains a dictionary with the fields:
"host", "services", "directories"

The field "host" has a string value representing the network address of the
host itself. If you can use this address to ssh into your host you are good
to go.

The field "services" contains a dictionary of services, that need special
treatment for backing up their data. Mainly it would be databases. Currently
supported services are: "mysql".

The field "directories" contains a list of directory paths on the host. Each
directory will be backed up recursively, not following symbolic links.

**Hint:**
All hosts will be mirrored to the "first_level_backup_directory", each
time the backup runs. There are no exceptions. So, even is a host is
not covered by any backup job, you will at least have a pretty current
copy of it's data on a different storage. But do not forget, to
add a newly added host to your backup jobs also.
