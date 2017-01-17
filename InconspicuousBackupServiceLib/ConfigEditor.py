#!/usr/bin/env python3
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

# Imports

import os
import json
import glob

CONFIGURATION_FOLDER_NAME = "conf"
GLOBAL_CONFIGURATION_FILE_NAME = "configuration.json"
HOSTS_CONFIGURATION_FOLDER_NAME = "hosts"
STORAGES_CONFIGURATION_FOLDER_NAME = "storages"
JOBS_CONFIGURATION_FOLDER_NAME = "jobs"
SCHEDULE_FOLDER_NAME = "schedule"

CONFIGURATION_FILE_NAME_PATTERN = "*.json"
CONFIGURATION_FILE_NAME_EXTENSION = ".json"

CONF_KEY_FIRST_LEVEL_BACKUP_DIRECTORY = "first_level_backup_directory"
CONF_KEY_REPORT_DIRECTORY = "report_directory"
CONF_KEY_EMAIL = "email"
CONF_KEY_SERVER = "server"
CONF_KEY_USERNAME = "username"
CONF_KEY_PASSWORD = "password"
CONF_KEY_FROM = "from"
CONF_KEY_TO = "to"
CONF_KEY_HOST = "host"
CONF_KEY_SERVICES = "services"
CONF_KEY_DIRECTORIES = "directories"
CONF_KEY_TYPE = "type"
CONF_KEY_STRATEGY = "strategy"
CONF_KEY_REQUIRED_CAPACITY = "required_capacity"
CONF_KEY_HDD = "hdd"
CONF_KEY_DIRECTORY = "directory"
CONF_KEY_MOUNTPOINT = "mountpoint"
CONF_KEY_DESCRIPTION = "description"
CONF_KEY_STORAGE = "storage"

BACKUP_STRATEGY_TGZ_LINEAR_FULL = "tgz-linear-full"
BACKUP_STRATEGY_TGZ_RINGBUFFER_FULL = "tgz-ringbuffer-full"
BACKUP_STRATEGY_RSYNC_LINEAR_INCREMENTAL = "rsync-linear-incremental"
BACKUP_STRATEGY_RSYNC_RINGBUFFER_INCREMENTAL = "rsync-ringbuffer-incremental"

SERVICE_TYPE_MYSQL = "mysql"
SERVICE_TYPE_POSTGRESQL = "pgsql"


class ConfigurationObject:

    def __init__(self, object_id="", config=None):
        self._id = object_id
        self._config = config
        
    def get_id(self):
        return self._id  
    
    def parse_json(self, json_string):
        self._config = json.loads(json_string)
    
    def get_json(self):
        json_string = json.dumps(self._config)
        return json_string
        
    def load_file(self, path):
        with open(path, "r") as file_handler:
            data = file_handler.read()
            self.parse_json(data)

    def write_file(self, path):
        json_string = self.get_json()
        with open(path, "w") as file_handler:
            file_handler.write(json_string)


class HostConfiguration(ConfigurationObject):
    
    def get_hostname(self):
        return self._config["host"]
    
    def set_hostname(self, hostname):
        self._config["host"] = hostname
     
    def get_mysql_service(self):
        try:
            return self._config["services"]["mysql"]
        except ValueError:
            return {}
            
    def set_mysql_service(self, username, password):
        self._config[CONF_KEY_SERVICES][SERVICE_TYPE_MYSQL] = {CONF_KEY_USERNAME: username,
                                                               CONF_KEY_PASSWORD: password}
    
    def get_directories(self):
        return self._config["directories"]
    
    def set_directories(self, directory_list):
        self._config["directories"] = directory_list
    
    def add_directory(self, path):
        self._config["directories"].append(path)


class StorageConfiguration(ConfigurationObject):
    
    def get_type(self):
        return self._config["type"]
    
    def set_type(self, storage_type):
        self._config["type"] = storage_type
      
    def get_required_capacity(self):
        return self._config["required_capacity"]
        
    def set_required_capacity(self, capacity):
        self._config["required_capacity"] = capacity
    
    
class JobConfiguration(ConfigurationObject):
    
    def get_host_id(self):
        return self._config["host"]
    
    def set_host_id(self, host_id):
        self._config[CONF_KEY_HOST] = host_id
        
    def get_storage_id(self):
        return self._config[CONF_KEY_STORAGE]
    
    def set_type(self, storage_id):
        self._config[CONF_KEY_STORAGE] = storage_id
        
    def get_description(self):
        return self._config[CONF_KEY_DESCRIPTION]
    
    def set_description(self, description):
        self._config[CONF_KEY_DESCRIPTION] = description

    
class ConfigurationDirectory:
    
    def __init__(self, path, template):
        self._template = template
        self._path = path
        self._list = []
        self.read()

    def get_list(self):
        return self._list
    
    def get_object(self, object_id):
        for element in self._list:
            if element.get_id() == object_id:
                return element
        return None

    def _create(self, object_id, config):
        element = self._template.__class__(obejct_id=object_id, config=config)
        self._list.append(element)
        return object 
    
    def delete(self, object_id):
        delete_element = None
        for element in self._list:
            if element.get_id() == object_id:
                delete_element = element
                break
        if delete_element is not None:
            self._list.remove(delete_element)

    def read(self):
        file_list = glob.glob(self._path, CONFIGURATION_FILE_NAME_PATTERN, recursive=False)
        for file_name in file_list:
            element = self._template.__class__(file_name)
            element.read_file(file_name)

    def write(self):
        for element in self._list:
            element.write_file(element.get_id())


class HostList(ConfigurationDirectory):
    
    def create(self, object_id, host_name, directories, services):
        config = {"host": host_name,
                  "directories": directories,
                  "services": services}
        self._create(object_id, config)


class StorageList(ConfigurationDirectory):

    def create(self, object_id, storage_type, strategy, required_capacity):
        config = {CONF_KEY_TYPE: storage_type,
                  CONF_KEY_STRATEGY: strategy,
                  CONF_KEY_REQUIRED_CAPACITY: required_capacity}
        self._create(object_id, config)


class JobList(ConfigurationDirectory):
    
    def create(self, object_id, description, host_id, storage_id):
        config = {CONF_KEY_HOST: host_id,
                  CONF_KEY_STORAGE: storage_id,
                  CONF_KEY_DESCRIPTION: description}
        self._create(object_id, config)
    
    def get_list_for_host(self, host_id):
        job_list = []
        for job in self.get_list():
            if job.get_host_id() == host_id:
                job_list.append(job)
        return job_list
        
    def get_list_for_storage(self, storage_id):
        job_list = []
        for job in self.get_list():
            if job.get_storage_id() == storage_id:
                job_list.append(job)
        return job_list


class Schedule:

    def __init__(self, schedule_path, jobs_path):
        self._schedule_path = schedule_path
        self._jobs_path = jobs_path


class ConfigurationEditor:

    def __init__(self, path):
        self._config_path = path
        self._host_list = HostList(os.path.join(path, HOSTS_CONFIGURATION_FOLDER_NAME),
                                   HostConfiguration())
        self._storage_list = HostList(os.path.join(path, STORAGES_CONFIGURATION_FOLDER_NAME),
                                      StorageConfiguration())
        self._job_list = HostList(os.path.join(path, JOBS_CONFIGURATION_FOLDER_NAME),
                                  JobConfiguration())
        self._schedule = Schedule(os.path.join(path, SCHEDULE_FOLDER_NAME),
                                  os.path.join(path, JOBS_CONFIGURATION_FOLDER_NAME))

    def get_schedule(self):
        return self._schedule

    def get_host_list(self):
        return self._host_list

    def get_storage_list(self):
        return self._storage_list

    def get_job_list(self):
        return self._job_list
