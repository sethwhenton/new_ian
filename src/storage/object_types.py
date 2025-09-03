#!/usr/bin/python3"
"""Object_type Model - Module"""
from sqlalchemy import String, Column, Text
from sqlalchemy.orm import relationship
from .base_model import Base, BaseModel

class Object_type(BaseModel, Base):
    """Creating an Object_type table in the database
    Args
        name: name of the object type
        description: A simple description of the object
    """
    __tablename__ = 'Object_type'
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(128), nullable=False)
    outputs = relationship("Output", backref="input_id", cascade="all, delete-orphan")

     def __init__(self):
        """initializes Object_type class"""
        super().__init__()
