""" 
# readers.text_readers.py
This module contains classes for reading text files in different formats.
Author: Balakrishna Maduru
"""
import json
import yaml
import csv

class ReadText():
    def read(self, file_path, file_system):
        return file_system.read_text(file_path)
    
class ReadJson():
    def read(self, file_path, file_system):
        return json.loads(file_system.read_text(file_path))
    
class ReadYaml():
    def read(self, file_path, file_system):
        return yaml.load(file_system.read_text(file_path), Loader=yaml.FullLoader)

class ReadCsv():
    def read(self, file_path, file_system):
        return csv.reader(file_system.read_text(file_path))

