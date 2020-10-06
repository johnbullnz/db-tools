from pathlib import Path
from configparser import ConfigParser

"""
Load config parameters
"""


class Config:
    def __init__(self, config_file):
        self.config_parser = ConfigParser()
        self.config_parser.read(config_file)

        self.username = self.get_config("username")
        self.password = self.get_config("password")
        self.url = self.get_config("url")
        self.port = self.get_config("port")
        self.connection_string = self.get_config("connection_string")
        self.database = self.get_config("database")
        self.ca_certificate_path = self.get_config("ca_certificate_path")
        self.backup_path = Path(self.get_config("backup_path", "/var/tmp"))

    def get_config(self, parameter, fallback=None):
        return self.config_parser.get("GENERAL", parameter, fallback=fallback)
