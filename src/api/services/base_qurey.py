from sqlalchemy import select, exists, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils import raise_http_exception


class BaseQuery:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def get_all_fields(self) -> Result:
        """
        Получить список всех полей объекта
        :return: Result
        """
        result = await self.session.execute(select(self.model))
        return result

    async def get_object_id_by_kwargs(self, model, **kwargs) -> Result:
        """
        Получить id объекта по параметрам
        :param model: модель
        :param kwargs: параметры для поиска, например "id=1"
        :return: Result
        """
        conditions = [getattr(model, key) == value for key, value in kwargs.items()]
        query = select(model.id).where(*conditions)
        result = await self.session.execute(query)
        return result

    async def get_object_by_kwargs(self, model, **kwargs) -> Result:
        """
        Получить объект или объекты по параметрам
        :param model: модель
        :param kwargs: параметры для поиска, например "id=1"
        :return: Result
        """
        conditions = [getattr(model, key) == value for key, value in kwargs.items()]
        query = select(model).where(*conditions)
        result = await self.session.execute(query)
        return result

    async def check_exists(self, model_name, **kwargs) -> bool:
        """
        Проверяет, существует ли объект с параметрами
        :param model_name: модель
        :param kwargs: параметры для поиска, например "id=1"
        :return: bool
        """
        conditions = [
            getattr(model_name, key) == value for key, value in kwargs.items()
        ]
        query = exists().where(*conditions).select()
        result = await self.session.scalar(query)
        return result

    async def check_exists_or_raise(
        self, model, status_code: int, exc_text: str | None = None, **kwargs
    ) -> None:
        """
        Проверяет, существует ли объект с параметрами, если нет - вызывает HTTPException
        :param model: модель
        :param status_code: код ошибки
        :param exc_text: текст ошибки, если не указан - будет сгенерирован автоматически
        :param kwargs: параметры для поиска, например "id=1"
        :return: None
        """
        check_exists = await self.check_exists(model_name=model, **kwargs)

        if not check_exists:

            exception_text = None
            if exc_text:
                exception_text = exc_text
            else:
                exception_text = f"{model.__name__} with {kwargs} does not exist"
            await raise_http_exception(status_code=status_code, detail=exception_text)
