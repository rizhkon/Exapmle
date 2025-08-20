from typing import Optional
from pydantic import BaseModel, RootModel
from typing import List


class Role2FileTypeBase(BaseModel):
    id: int
    role_group_id: Optional[int] = None
    file_type_id: Optional[int] = None


class PutRole2FileTypeData(BaseModel):
    id: int
    role_group_id: Optional[int] = None
    file_type_id: Optional[int] = None


class PostRole2FileTypeData(BaseModel):
    id: Optional[int] = None
    role_group_id: int
    file_type_id: int


class Role2FileTypeBaseWithoutID(BaseModel):
    role_group_id: int
    file_type_id: int


class RoleFileTypeList(RootModel[List[Role2FileTypeBaseWithoutID]]):
    pass
