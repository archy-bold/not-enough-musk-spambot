#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def read_env(key: str, default: str=None) -> str:
    val: str = os.getenv(key, default)
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
