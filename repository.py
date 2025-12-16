from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.books import BookModel
from schemas.books import SBookAdd


class BooksRepository:
    @classmethod
    async def add_book(cls, book: SBookAdd, session: AsyncSession):
        book_dict = book.model_dump()
        new_book = BookModel(**book_dict)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    @classmethod
    async def get_all_books(cls, session: AsyncSession):
        stmt = select(BookModel)
        books = await session.scalars(stmt)
        return books.all()

    @classmethod
    async def get_book(cls, book_id: int, session: AsyncSession):
        stmt = select(BookModel).where(BookModel.id == book_id)
        book = await session.scalars(stmt)
        return book.one_or_none()

    @classmethod
    async def update_book(cls, book_id: int, book: SBookAdd, session: AsyncSession):
        stmt = select(BookModel).where(BookModel.id == book_id)
        book_db = await session.scalars(stmt)
        if book_db.first():
            book_data = book.model_dump()
            book_data["id"] = book_id
            stmt = update(BookModel).where(BookModel.id == book_id).values(book_data)
            await session.execute(stmt)
            await session.commit()
            return book_data

    @classmethod
    async def delete_book(cls, book_id: int, session: AsyncSession):
        stmt = select(BookModel).where(BookModel.id == book_id)
        result = await session.scalars(stmt)
        if result.first():
            await session.execute(delete(BookModel).where(BookModel.id == book_id))
            await session.commit()
            return True
