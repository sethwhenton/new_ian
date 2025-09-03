#!/usr/bin/python3
"""create a unique Storage instance for the application"""
from .engine import engine
from .base_model import BaseModel
from os import getenv


# load from database
db = getenv('HH_MYSQL_DB')
if db:
    engine = engine.Engine()
    engine.reload()
