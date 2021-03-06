# Directory "./conf/storages/"

In this directory you create a ".json" file for each backup storage device that
is connected to your backup server.

For hard-disk like backup devices, which are written to by using a file system path,
its recommended to use file names similar to those paths. Just replace each "/"
with an underscore "_". Here are some examples:
* /mnt/backup_hdd1              => mnt_backup_hdd1
* /media/usb_hdd/               => media_usb_hdd
* /media/network/backup_on_nas1 => media_network_backup_on_nas1

For stream devices the same pattern can be applied to the devices path:
* /dev/nst0 => dev_nst0

Supported storage types with corresponding strategies are:
* "hdd" - Use a mounted, writable file system, usually a hard disk drive.
  * "tgz-linear-full" - Create a .tar.gz archive with each backup.
  * "tgz-ringbuffer-full" - Create a .tar.gz archive with each backup. Delete oldest backup, if there are more archives "required_capacity" defines. 
  * "rsync-linear-incremental" - Create a directory with each backup. Copy changed files only. Create hardlinks to older backups for unchanged files. 
  * "rsync-ringbuffer-incremental" - Create a directory with each backup. Copy changed files only. Create hardlinks to older backups for unchanged files. Delete oldest backup, if there are more archives "required_capacity" defines.

Each storage type has its own set of parameters:
* "hdd"
  * "directory" - The directory where backups will be stored.
  * "mountpoint" - The directory where the drive is mounted to.

The content of a file might look like this:
```javascript
{
    "type" : "hdd",
    "strategy" : "tgz-ringbuffer-full",
    "required_capacity" : 5,
    "hdd" : {
        "directory" : "/mnt/backup_hdd1" ,
        "mountpoint" : "/mnt/backup_hdd1"
     }
}
```
As you might have noticed the files are in JSON format. You 'll find information
about the format itself on: https://en.wikipedia.org/wiki/JSON

Each file contains a dictionary with the fields:

...TO BE CONTINUED ...
