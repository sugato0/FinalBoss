from datetime import date  # работа с датами

from sqlalchemy import Integer, String, Date, Boolean, select  # типы и select (новый стиль запросов)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  # асинхронный движок и сессии
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  # база ORM и описание колонок


engine = create_async_engine("sqlite+aiosqlite:///tasks.db")  # асинхронное подключение к sqlite через aiosqlite
Session = async_sessionmaker(bind=engine, expire_on_commit=False)  # фабрика асинхронных сессий


class Base(DeclarativeBase):  # базовый класс от которого наследуются таблицы (Не обращай внимания)
    pass


class DayTask(Base):
    __tablename__ = "day_tasks"  # название таблицы
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # уникальный id
    title: Mapped[str] = mapped_column(String, nullable=False)  # название задачи обязательно
    description: Mapped[str | None] = mapped_column(String)  # описание может быть пустым
    task_date: Mapped[date] = mapped_column(Date, nullable=False)  # дата задачи
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)  # выполнена или нет


async def create_tables() -> None:
    async with engine.begin() as conn:  # открываем соединение
        await conn.run_sync(Base.metadata.create_all)  # создаем таблицы если их нет

#вот тут добавление задачи
async def add_task(
    title: str,
    description: str | None = None,
    task_date: date | None = None
) -> int:
    async with Session() as session:  # открываем асинхронную сессию
        task = DayTask(
            title=title,
            description=description,
            task_date=task_date or date.today()  # если дата не передана ставим сегодня
        )

        session.add(task)  # добавляем объект в бд
        await session.commit()  # сохраняем изменения

        return task.id  # возвращаем id задачи

#вот тут получение задачи
async def get_tasks(task_date: date | None = None) -> list[DayTask]:
    async with Session() as session:  # открываем сессию
        query = select(DayTask)  # формируем запрос

        if task_date is not None:
            query = query.where(DayTask.task_date == task_date)  # фильтр по дате

        query = query.order_by(DayTask.id)  # сортировка

        result = await session.execute(query)  # выполняем запрос

        return list(result.scalars().all())  # достаем объекты из результата

#вот тут обновление задачи по id
async def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    task_date: date | None = None,
    is_done: bool | None = None
) -> bool:
    async with Session() as session:  # открываем сессию
        task = await session.get(DayTask, task_id)  # ищем задачу по id

        if task is None:
            return False  # если не нашли

        if title is not None:
            task.title = title  # обновляем название

        if description is not None:
            task.description = description  # обновляем описание

        if task_date is not None:
            task.task_date = task_date  # обновляем дату

        if is_done is not None:
            task.is_done = is_done  # обновляем статус

        await session.commit()  # сохраняем изменения

        return True

#вот тут удаление задачи по id
async def delete_task(task_id: int) -> bool:
    async with Session() as session:  # открываем сессию
        task = await session.get(DayTask, task_id)  # ищем задачу

        if task is None:
            return False  # если нет такой задачи

        await session.delete(task)  # удаляем объект
        await session.commit()  # фиксируем удаление

        return True