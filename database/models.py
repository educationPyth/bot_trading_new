from sqlalchemy import BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(255))


class UserBot(Base):
    __tablename__ = 'user_bots'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat: Mapped[str] = mapped_column(String(255))
    contract: Mapped[str] = mapped_column(String(255))
    photo: Mapped[str] = mapped_column(String(255))
    links: Mapped[str] = mapped_column(String(255))
    title_channel: Mapped[str] = mapped_column(String(255))
    transactions_time = mapped_column(BigInteger)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

