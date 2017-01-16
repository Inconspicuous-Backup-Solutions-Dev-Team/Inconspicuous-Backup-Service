# ----------------------------------------------------------------------------------------------------------------------
# Inconspicuous Backup Service
#
# Copyright 2016 by Inconspicuous Backup Solutions Dev. Team, Christian Beuschel <chris109@web.de>
#
# This file is part of Inconspicuous Backup Service.
#
# Inconspicuous Backup Service is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Inconspicuous Backup Service is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License along with Inconspicuous Backup Service. If not,
# see <http://www.gnu.org/licenses/>.
# 
# ----------------------------------------------------------------------------------------------------------------------

============================
Directory "./conf/storages/"
============================

In this directory you create a ".json" file for each backup storage device that
is connected to your backup server.

For hard-disk like backup devices, which are written to by using a file system path,
its recommended to use file names similar to those paths. Just replace each "/"
with an underscore "_". Here are some examples:
/mnt/backup_hdd1              => mnt_backup_hdd1
/media/usb_hdd/               => media_usb_hdd
/media/network/backup_on_nas1 => media_network_backup_on_nas1

For streaming devices the same pattern can be applied to the devices path:
/dev/nst0 => dev_nst0

The content of a file might look like this:

{
    "type" : "hdd",
    "strategy" : "fullring",
    "required_capacity" : 5,
    "hdd" : {
        "directory" : "/mnt/backup_hdd1" ,
        "mountpoint" : "/mnt/backup_hdd1"
     }
}

As you might have noticed the files are in JSON format. You 'll find information
about the format itself on: https://en.wikipedia.org/wiki/JSON

Each file contains a dictionary with the fields:

...TO BE CONTINUED ...
