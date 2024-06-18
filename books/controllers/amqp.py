from dishka.entities.depends_marker import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from books.application.dto import NewBookDTO
from books.application.interactors import NewBookInteractor
from books.controllers.schemas import BookSchema


AMQPBookController = RabbitRouter()

@AMQPBookController.subscriber("create_book")
@AMQPBookController.publisher("book_statuses")
async def handler(data: BookSchema, interactor: Depends[NewBookInteractor]) -> str:
    dto = NewBookDTO(
        title=data.title,
        pages=data.pages,
        is_read=data.is_read
    )
    uuid = await interactor(dto)
    return uuid
