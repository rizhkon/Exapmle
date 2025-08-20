from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select, Row, RowMapping
from src.api.models import Role2FileType
from src.api.schemas.role2_file_type_schemas import (
    PutRole2FileTypeData,
    Role2FileTypeBaseWithoutID,
    RoleFileTypeList,
)
from src.api.services.base_qurey import BaseQuery


class Role2FileTypeQuery(BaseQuery):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Role2FileType)

    async def get_all_file_type_by_role_id(self, **kwargs) -> list:
        """
        Получить список связей между ролью и типами файлов.

        :param kwargs: параметры для поиска, например "role_group_id=1"
        :return: list
        """
        result = (
            (await self.get_object_by_kwargs(model=self.model, **kwargs))
            .scalars()
            .all()
        )

        filtered_result = [
            Role2FileTypeBaseWithoutID(**obj.__dict__).model_dump() for obj in result
        ]
        return filtered_result

    async def get_role_group_id_and_file_type_id_by_id(
        self, id: int
    ) -> Row | RowMapping | None:
        """
        Получить связь между ролью и типами файлов по id.

        :param id: id связи
        :return: Row | RowMapping | None
        """
        await self.check_exists_or_raise(model=self.model, status_code=404, id=id)
        result = await self.get_object_by_kwargs(self.model, id=id)
        return result.scalars().first()


    async def post_role2_file_type_by_list(self, data: RoleFileTypeList) -> None:
        """
        Изменить связь между ролью и типами файлов по id.

        :param data: параметры для создания
        :return: None
        """
        for record in data.root:
            existing_record = await self.session.execute(
                select(Role2FileType).where(
                    Role2FileType.role_group_id == record.role_group_id,
                    Role2FileType.file_type_id == record.file_type_id,
                )
            )
            existing_record = existing_record.scalars().first()
            if existing_record:
                continue
            record = Role2FileType(
                role_group_id=record.role_group_id, file_type_id=record.file_type_id
            )
            self.session.add(record)
        await self.session.commit()
        return


    async def put_role2_file_type(self, data: PutRole2FileTypeData) -> Role2FileType:
        """
        Обновить связь между ролью и типами файлов по id.

        :param data: параметры для обновления
        :return: Role2FileType
        """
        await self.check_exists_or_raise(
            model=self.model, status_code=404, id=data["id"]
        )

        record = (
            await self.get_object_by_kwargs(model=self.model, id=data["id"])
        ).scalar_one()

        record_id = data.pop("id")
        await self.session.execute(
            update(Role2FileType).where(Role2FileType.id == record_id).values(**data)
        )
        await self.session.commit()
        await self.session.refresh(record)
        return record


    async def delete_role2_file_type(self, data: RoleFileTypeList) -> None:
        """
        Удалить связь между ролью и типами файлов по id.

        :param data: параметры для удаления
        :return: None
        """
        for record in data.root:
            await self.session.execute(
                delete(Role2FileType).where(
                    Role2FileType.file_type_id == record.file_type_id,
                    Role2FileType.role_group_id == record.role_group_id,
                )
            )
        await self.session.commit()
        return
