from typing import Protocol

from books.domain.entities import Book


class BookSaver(Protocol):
    async def save(self, book: Book) -> None:
        ...


class BookReader(Protocol):
    async def read_by_uuid(self, uuid: str) -> Book | None:  
        ...  


class DBSession(Protocol):  
    async def commit(self) -> None:  
        ...  
  
    async def flush(self) -> None:  
        ...
