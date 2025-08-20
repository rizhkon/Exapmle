from fastapi import APIRouter, Depends, Query
from src.api.schemas.role2_file_type_schemas import (
    Role2FileTypeBase,
    PutRole2FileTypeData,
    RoleFileTypeList,
)
from src.api.services.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v3", tags=["CRUD для Role2FileType"])


@router.get(
    "/getRole2FileType",
    response_model=Role2FileTypeBase,
    status_code=200,
    summary="Получить свзяь по id",
)
async def get_role_group_id_and_file_type_id_by_id(
    id: int = Query(...), uow: UnitOfWork = Depends(get_uow)
) -> Role2FileTypeBase:
    result = await uow.role2_file_type.get_role_group_id_and_file_type_id_by_id(id=id)
    return result


@router.get(
    "/getAllFileTypeByRoleId",
    status_code=200,
    summary="Получить все fileType по RoleId",
)
async def get_all_file_type_by_role_id(
    role_group_id: int = Query(...), uow: UnitOfWork = Depends(get_uow)
) -> list:
    result = await uow.role2_file_type.get_all_file_type_by_role_id(
        role_group_id=role_group_id
    )
    return result


@router.post(
    "/createRole2FileTypeByList",
    status_code=201,
    summary="Создать связь прав доступа роли к Типам файлов",
)
async def create_role2_file_type_by_id_list(
    data: RoleFileTypeList, uow: UnitOfWork = Depends(get_uow)
) -> None:
    await uow.role2_file_type.post_role2_file_type_by_list(data=data)
    return


@router.put(
    "/updateRole2FileType",
    response_model=Role2FileTypeBase,
    status_code=200,
    summary="Обновить связь прав доступа роли к Типам файлов",
)
async def update_role2_file_type(
    data: PutRole2FileTypeData, uow: UnitOfWork = Depends(get_uow)
) -> Role2FileTypeBase:
    result = await uow.role2_file_type.put_role2_file_type(
        data=data.model_dump(exclude_none=True, exclude_unset=True)
    )
    return result


@router.delete(
    "/deleteRole2FileType",
    status_code=204,
    summary="Удалить связь прав доступа роли к Типам файлов",
)
async def delete_role2_file_type(
    data: RoleFileTypeList, uow: UnitOfWork = Depends(get_uow)
) -> None:
    await uow.role2_file_type.delete_role2_file_type(data=data)
    return
