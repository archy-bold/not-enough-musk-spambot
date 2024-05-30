#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv

# Read flags
def load_env_from_flags(parser: argparse.ArgumentParser=None) -> None:
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument("-env", "--env-file", dest = "env_file", default = None, help="The .env file")

    if parser.parse_args().env_file is None:
        print("Loading environment variables from .env...")
    else:
        if not os.path.isfile(parser.parse_args().env_file):
            print("Could not find .env file at " + parser.parse_args().env_file)
            exit(1)
        print("Loading environment variables from " + parser.parse_args().env_file + "...")
    load_dotenv(parser.parse_args().env_file)

def read_env(key: str, default: str=None, secret: bool=False) -> str:
    val: str = os.getenv(key, default)
    if secret:
        print(key + "=********")
    else:
        print(key + "=" + val)
    return val

def read_env_float(key: str, default: float=None) -> float:
    val: float = float(os.getenv(key, default))
    print(key + "=" + str(val))
    return val

def read_env_int(key: str, default: int=None) -> int:
    val: int = int(os.getenv(key, default))
    print(key + "=" + str(val))
    return val
