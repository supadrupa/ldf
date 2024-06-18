from typing import AsyncIterable

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from books.application import interfaces
from books.application.interactors import (
    GetBookInteractor,
    NewBookInteractor
)
from books.config import Config
from books.infrastructure.database import new_session_maker
from books.infrastructure.gateways import BookGateway


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        interfaces.DBSession,
    ]]:
        async with session_maker() as session:
            yield session

    book_gateway = provide(  
        BookGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.BookReader, interfaces.BookSaver]
    )

    get_book_interactor = provide(GetBookInteractor, scope=Scope.REQUEST)
    create_new_book_interactor = provide(NewBookInteractor, scope=Scope.REQUEST)
