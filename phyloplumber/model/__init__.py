"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm, schema
from sqlalchemy.ext.declarative import declarative_base
from phyloplumber.model import meta

def now():
    return datetime.datetime.now()

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    #meta.Session.configure(bind=engine)
    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    meta.set_metadata(schema.MetaData(bind=engine))


    t_group = schema.Table("PhyloplumberGroup", meta.get_metadata(),
        schema.Column('id', sa.types.Integer,
            schema.Sequence('groupuser_seq_id', optional=True), primary_key=True),
        sa.Column("name", sa.types.String, nullable=False),
        )
    
    t_user = schema.Table("PhyloplumberUser", meta.metadata,
        schema.Column('id', sa.types.Integer,
            schema.Sequence('groupuser_seq_id', optional=True), primary_key=True),
        sa.Column("username", sa.types.String, nullable=False),
        sa.Column("fullname", sa.types.String, nullable=False),
        sa.Column("date_created", sa.types.DateTime, nullable=False),
        sa.Column("email", sa.types.DateTime, nullable=False),
        )
    
    t_process = schema.Table("ExternalProcess", meta.metadata,
        sa.Column("id", sa.types.String, nullable=False, primary_key=True),
        sa.Column("parent_dirname", sa.types.String, nullable=False),
        sa.Column("launch_timestamp", sa.types.DateTime, nullable=False),
        sa.Column("invocation", sa.types.String, nullable=False),
        sa.Column("label", sa.types.String, nullable=False),
        sa.Column("status", sa.types.Integer, nullable=False),
        sa.Column("service_name", sa.types.String, nullable=False), # this is the controller that launched the job
        sa.Column("read_group", sa.types.Integer, schema.ForeignKey('PhyloplumberGroup.id')),
        sa.Column("write_group", sa.types.Integer, schema.ForeignKey('PhyloplumberGroup.id')),
        )
    
    
    
    t_group_user = schema.Table('PhyloplumberGroupUser', meta.metadata,
        schema.Column('id', sa.types.Integer,
            schema.Sequence('groupuser_seq_id', optional=True), primary_key=True),
        schema.Column('groupid', sa.types.Integer, schema.ForeignKey('PhyloplumberGroup.id')),
        schema.Column('userid', sa.types.Integer, schema.ForeignKey('PhyloplumberUser.id')),
    )
    
    
    class PhyloplumberGroup(object):
        pass
    class PhyloplumberUser(object):
        pass
    class PhyloplumberGroupUser(object):
        pass
    class ExternalProcess(object):
        pass
    
    orm.mapper(PhyloplumberGroup, t_group)
    orm.mapper(PhyloplumberUser, t_user)
    orm.mapper(ExternalProcess, t_process)
    orm.mapper(PhyloplumberGroupUser, t_group_user)

