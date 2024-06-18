from dataclasses import dataclass


@dataclass(slots=True)  
class Book:
    uuid: str  
    title: str  
    pages: int  
    is_read: bool
