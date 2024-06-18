from books.domain.entities import Book
from books.application.interfaces import BookSaver, BookReader, DBSession
from books.application.dto import NewBookDTO
from uuid import uuid4


class NewBookInteractor:
    def __init__(
            self,
            db_session: DBSession,
            book_gateway: BookSaver,
    ):
        self._db_session = db_session
        self._book_gateway = book_gateway

    async def __call__(self, book_dto: NewBookDTO):
        uuid = str(uuid4())
        
        book = Book(
            uuid=uuid,
            title=book_dto.title,
            pages=book_dto.pages,
            is_read=book_dto.is_read,
        )
        await self._book_gateway.save(book)
        await self._db_session.commit()
        return uuid


class GetBookInteractor:
    def __init__(self, book_gateway: BookReader):
        self._book_gateway = book_gateway

    async def __call__(self, book_uuid):
        return await self._book_gateway.read_by_uuid(book_uuid)
