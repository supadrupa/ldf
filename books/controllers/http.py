from typing import Annotated
from uuid import UUID

from dishka.entities.depends_marker import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, route, HttpMethod, status_codes
from litestar.exceptions import HTTPException
from litestar.params import Body

from books.controllers.schemas import BookSchema
from books.application.interactors import GetBookInteractor


class HTTPBookController(Controller):
    path = "/book"

    @route(http_method=HttpMethod.GET, path="/{book_id:uuid}")
    @inject
    async def get_book(
        self, 
        book_id: Annotated[UUID, Body(description="Book ID", title="Book ID")], 
        interactor: Depends[GetBookInteractor]
    ) -> BookSchema:
        book = await interactor(book_uuid=str(book_id))

        if not book:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        return BookSchema(
            title=book.title,
            pages=book.pages,
            is_read=book.is_read,
        )
