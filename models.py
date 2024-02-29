import os
from sqlalchemy import String, ForeignKey, DateTime, func

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import datetime

POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'db_dc')

PG_DNS = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DNS)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class User(Base):
    __tablename__ = 'aiohttp_user'   
							
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, 	index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), unique=False, 	nullable=False) 

    @property 
    def make_dict(self):
        user_data = {	
			'id': self.id,	
			'name': self.name,	
			'password': self.password
			}		
        return user_data

class Advertisement(Base):
    __tablename__ = 'aiohttp_adv'   

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(200))
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[int] = mapped_column(ForeignKey('aiohttp_user.id'))

    @property 
    def make_dict(self):
        adv_data = {	
			'id': self.id,	
			'title': self.title,	
			'description': self.description,
            'created': self.created.isoformat(),
            'owner': self.owner
			}		
        return adv_data


async def init_db():
    print('work init_db')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
