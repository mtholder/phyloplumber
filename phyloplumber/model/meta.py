"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import schema


__all__ = ['Base', 'Session']

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

metadata = None
def get_metadata():
    global metadata
    return metadata
def set_metadata(n):
    global metadata
    metadata = n

# Assign the same metadata object we created earlier.
#Base = declarative_base(metadata=metadata)



