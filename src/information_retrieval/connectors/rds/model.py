from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import DDL


Base = declarative_base()
N_DIM = 1024


class TableArgsMixin:
    __table_args__ = {"extend_existing": True}


class Users(Base, TableArgsMixin):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    email = Column(Text, nullable=False, unique=True)
    data = Column(JSONB, nullable=False, server_default='{}')
    created_on = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_on = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Documents(Base):
    __tablename__ = 'documents'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False, server_default='')
    question = Column(Text)
    document_type = Column(Text)
    data = Column(JSONB, nullable=False, server_default='{}')
    created_on = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_on = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("Users")


async def create_extensions(conn):
    await conn.execute(DDL("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))


async def create_update_triggers(conn):
    await conn.execute(DDL("""
        CREATE OR REPLACE FUNCTION update_updated_on_column()
        RETURNS TRIGGER AS $update_updated_on_column$ BEGIN NEW.updated_on = (now() at time zone 'utc'); 
        RETURN NEW; END; $update_updated_on_column$ language 'plpgsql';
        """))


async def create_users_trigger(conn):
    await conn.execute(DDL("""
        CREATE TRIGGER trig_users_updated_on BEFORE INSERT OR UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
        """))


async def create_interviews_trigger(conn):
    await conn.execute(DDL("""
        CREATE TRIGGER trig_interviews_updated_on BEFORE INSERT OR UPDATE ON documents FOR EACH ROW EXECUTE PROCEDURE update_updated_on_column();
        """))
