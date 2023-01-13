from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from bot.misc.settings import SETTING_DB

dsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################

# create async engine for interaction

# engine = create_async_engine(SETTING_DB, future=True, echo=True)
engine = create_async_engine(dsn, future=True, echo=True)

# create async session for the interaction with database

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# base model

Base = declarative_base()

