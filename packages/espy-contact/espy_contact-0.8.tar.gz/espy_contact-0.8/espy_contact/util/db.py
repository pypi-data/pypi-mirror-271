from .CONSTANTS import SCHEMA
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData(schema=SCHEMA)
Base = declarative_base(metadata=metadata)