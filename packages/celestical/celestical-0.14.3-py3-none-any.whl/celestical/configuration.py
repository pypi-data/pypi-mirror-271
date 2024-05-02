# Managing the configuration for the Celestical services
import json
import os
import logging
import importlib.metadata
from logging import Logger
from pathlib import Path

import typer
from prettytable import PrettyTable, ALL

import celestical.api as api
from celestical.helper import print_text

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
apiconf = api.Configuration(
        host = "https://moon.celestical.net"
)

current_celestical_version = importlib.metadata.version('celestical')

# LOGGING_LEVEL = logging.DEBUG
# logging.basicConfig(encoding='utf-8', level=LOGGING_LEVEL)

HOTLINE = "starship@celestical.net"
PRODUCTION = True


def get_login_status() -> str:
    login_status = ""
    # [{wcol}]colored text[/{wcol}]
    wcol = "purple"

    udata = load_config()
    if not (udata is None or udata == {}):
        # else message that config cannot be loaded will be shown.
        tok = udata["access_token"]
        uname = udata["username"]
        if uname != "":
            login_status += f"\n\t* Current user: [{wcol}]{uname}[/{wcol}]"
        else:
            login_status += f"\n\t* No current user [{wcol}]logged in[/{wcol}]"
        if tok != "":
            # TODO checked the created date field to announce
            # if relogging is necessary.
            login_status += f"\n\t* [{wcol}]Already logged in[/{wcol}] once"

    return login_status


def welcome(verbose:int=2) -> str:
    """ Return a global welcome message

        verbose from 0 (short) to 2 (long)
    """
    wcol = "purple"
    welcome_message:str = f"[{wcol}]Direct deployment of containers or compose" \
                          +" files to an independent green cloud made by space" \
                          +f" engineers[/{wcol}] " \
                          +f"(version: {current_celestical_version})\n"

    if verbose > 0:
        welcome_message += get_login_status()


    if verbose > 1:
        welcome_message += "\n [underline]Usual workflow steps[/underline]" \
                        +"\n\t [1] (only once) Register with command " \
                        +f"[{wcol}]celestical register[/{wcol}]" \
                        +"\n\t [2] Login with command " \
                        +f"[{wcol}]celestical login[/{wcol}]" \
                        +"\n\t [3] Deploy with command " \
                        +f"[{wcol}]celestical deploy[/{wcol}]"

    return welcome_message


# Service types definitions
def get_default_config_dir() -> Path:
    path = Path.home() / ".config" / "celestical"
    return path


def get_default_config_path() -> Path:
    """Return the default config path for this application

    Returns:
        Path typed path to the config json file
    """
    path = get_default_config_dir() / "config.json"
    return path


def get_default_log_path() -> Path:
    """Return the default log file path for this application

    Returns:
        Path typed path to the log file
    """
    path = get_default_config_dir() / "celestical.log"
    return path


def load_config(config_path: str = "") -> dict:
    """Load config file from config_path.

    Params:
        config_path(str): non-default absolute path of the configuration.
    Returns:
        (dict): configuration content
    """
    path = get_default_config_path()
    if config_path is not None and config_path != "":
        path = Path(config_path)

    user_data = {}
    if path.exists():
        try:
            with open(path, 'r') as f_desc:
                user_data = json.load(f_desc)
        except:
            print_text("Could not read the configuration file.")
    # Useless too much info for user experience
    #else:
    #    print_text("The configuration file does not exist yet.")

    return user_data


def save_config(config:dict) -> bool:
    """Save config file to the default_config_path.

    Params:
        config(dict): configuration.
    Returns:
        (bool): True if saving process went fine
    """
    cpath = get_default_config_path()

    try:
        if not cpath.parent.exists():
            os.makedirs(cpath.parent, exist_ok=True)
    except Exception as oops:
        cli_logger.debug("save_config: directory couldn't be created.")
        cli_logger.debug(oops)
        return False

    try: 
        with open(cpath, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as oops:
        cli_logger.debug("save_config: config file couldn't be written.")
        cli_logger.debug(oops)
        return False

    return True


def cli_setup() -> bool:
    """ Setup necessary directories.
    """
    config_path = get_default_config_dir()
    try:
        config_path.mkdir(parents=True, exist_ok=True)
    except Exception as oops:
        return False
    return True


def create_logger(production: bool=False) -> Logger :
    """A function to create and configure the logger for the Celestical CLI
    Params:
        production(bool): if False, set log level to debug
    Returns:
        (logger): the logger object
    """
    log_format = "%(asctime)s --%(levelname)s: %(message)s"
    log_location = get_default_log_path()
    if production is False:
        logging.basicConfig(
            encoding='utf-8',
            filename=log_location,
            format=log_format,
            filemode="a",
            level=logging.DEBUG,
        )
        logger = logging.getLogger(name="Celestical CLI")
        logger.warning(f"Starting Logger in DEBUG Mode: {log_location}")
        return logger

    logging.basicConfig(
        encoding='utf-8',
        filename=log_location,
        format=log_format,
        filemode="a",
        level=logging.WARNING,
    )
    logger = logging.getLogger(name="Celestical CLI")
    logger.warning(f"Starting Logger in WARNING Mode: {log_location}")
    return logger

cli_setup()
# Creation of the CLI-wide logger -> celestical.log
cli_logger = create_logger(production=PRODUCTION)
