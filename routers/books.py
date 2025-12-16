from fastapi import APIRouter, status, HTTPException
from schemas.books import SBookAdd, SBook
from repository import BooksRepository
from database import SessionDep

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[SBook])
async def get_books(session: SessionDep):
    return await BooksRepository.get_all_books(session)


@router.get("/{id:int}", response_model=SBook)
async def get_book(id: int, session: SessionDep):
    if not (result := await BooksRepository.get_book(id, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return result


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_book(book: SBookAdd, session: SessionDep):
    return await BooksRepository.add_book(book, session)


@router.put("/{id:int}", response_model=SBook)
async def update_book(id: int, book: SBookAdd, session: SessionDep):
    if not (updated_book := await BooksRepository.update_book(id, book, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return updated_book


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, session: SessionDep):
    if not (result := await BooksRepository.delete_book(id, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
