"""
# file_system/file_system.py
This module provides a file system class that can be used to perform file system operations.
A file system is a method of storing, organizing and accessing files and directories on a storage device or network.
Author: Balakrishna Maduru
"""
import os
import yaml
import fsspec
from unified_fs.operations import Operations
from pathlib import Path
from . import file_system_path

class FileSystem(Operations):
    def __init__(self, source = None, destination = None):
        super().__init__()
        self._source_fs = None
        self._destination_fs = None
        self.source_fs = source
        self.destination_fs = destination if destination else source
        self._file_extension_mapping = yaml.load(open(f'{file_system_path}/config/file_extension_mapping.yaml'), Loader=yaml.FullLoader)

    @property
    def file_extension_mapping(self):
        return self._file_extension_mapping
    
    @file_extension_mapping.setter
    def file_extension_mapping(self, mapping):
        self._file_extension_mapping = mapping

    @property
    def source_fs(self):
        return self._source_fs
    
    @source_fs.setter
    def source_fs(self, info):
        if isinstance(info, dict):
            type = info.get('type', 'file')
            del info['type']
            self._source_fs = fsspec.filesystem(type,**info)
        else:
            self._source_fs = fsspec.filesystem(info)
        self._destination_fs = self._destination_fs if self._destination_fs else self._source_fs

    @property
    def destination_fs(self):
        return self._destination_fs
    
    @destination_fs.setter
    def destination_fs(self, info):
        if isinstance(info, dict):
            type = info.get('type', 'file')
            del info['type']
            self._destination_fs = fsspec.filesystem(type,**info)
        else:
            self._destination_fs = fsspec.filesystem(info)
        self._source_fs = self._source_fs if self._source_fs else self._destination_fs

    def import_class(self, class_path):
        print(f"class_path = {class_path}")
        module_name, class_name = class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)

    def read(self, file_path, file_system=None):
        print(f"Path(file_path).suffix = {Path(file_path).suffix}")
        class_name = self.file_extension_mapping.get(Path(file_path).suffix, "None")
        if class_name:
            class_instance = self.import_class(class_name)
            if file_system:
                return class_instance().read(file_path, file_system)
            else:
                return class_instance().read(file_path, self.source_fs)
        else:
            raise ValueError(f"File extension {Path(file_path).suffix} is not supported.")