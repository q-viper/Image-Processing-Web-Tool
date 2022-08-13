"""Module to define global variables.
"""
import json
import inspect
import os


class Variables:
    """A class to read config file and hold variables.
    """
    
    # Reading paths
    curr_dir = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    root_dir = os.path.dirname(curr_dir)
    conf_dir = os.path.join(root_dir, "config")

    # Reading Config file path
    config_file_path = os.path.join(conf_dir, "config.json")
    path = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Reading and loading config file
    with open(config_file_path, "r") as file:
        config = json.load(file)

    # logging variables
    logging = config["logging"]
    level = logging["level"]
    console_log = logging["console_log"]
    version = config["version"]

    # allowed modes
    allowed_modes_dict = config["allowed_modes"]
    allowed_modes = list(allowed_modes_dict.keys())

    def __getitem__(self, key):
        """Get the value from key."""
        return self.config[key]


try:
    var = Variables()
except Exception as err:
    raise err