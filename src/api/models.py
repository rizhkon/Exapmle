import uuid
from typing import Any
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Float,
    UUID,
    BigInteger,
    MetaData,
    text,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData(schema="stg")
Base: Any = declarative_base(metadata=metadata)


class RoleTypeList(Base):
    __tablename__ = "RoleTypeList"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('stg.\"attributeTypeList_id_seq\"'::regclass)"),
    )
    code = Column(String)
    name = Column(String)


class RoleGroupList(Base):
    __tablename__ = "RoleGroupList"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('stg.role_group_id_seq'::regclass)"),
    )
    name = Column(String)
    roleTypeId = Column(ForeignKey("stg.RoleTypeList.id", ondelete="CASCADE"))
    role_to_file_type = relationship(
        "Role2FileType", back_populates="role", cascade="all, delete"
    )
    role_to_root_list = relationship(
        "Role2RootList", back_populates="role", cascade="all, delete"
    )
    role_to_dictionary = relationship(
        "Role2DictionaryValue", back_populates="role", cascade="all, delete"
    )
    role_to_directory = relationship(
        "Role2Directory", back_populates="role", cascade="all, delete"
    )

    RoleTypeList = relationship("RoleTypeList")
    isQgisUser = Column(Boolean, default=False, name="isQgisUser")


class UserList(Base):
    __tablename__ = "UserList"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('stg.\"UserList_id_seq\"'::regclass)"),
    )
    login = Column(String, unique=True)
    firstName = Column(String)
    secondaryName = Column(String)
    email = Column(String)
    createDate = Column(DateTime)
    roleGroupId = Column(ForeignKey("stg.RoleGroupList.id"), nullable=False)
    passwd = Column(String)

    RoleGroupList = relationship("RoleGroupList")


class FileType(Base):
    __tablename__ = "FileType"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updateDate"
    )
    create_user = Column(String, name="createUser", nullable=True)
    update_user = Column(String, name="updateUser", nullable=True)
    file_list = relationship(
        "FileList", back_populates="file_type", cascade="all, delete"
    )
    file_type_to_attribute = relationship(
        "FileType2Attribute", back_populates="file_type", cascade="all, delete"
    )
    rules = relationship("Rules", back_populates="file_type", cascade="all, delete")
    role_to_file_type = relationship(
        "Role2FileType", back_populates="file_type", cascade="all, delete"
    )
    is_prognostic_data = Column(Boolean, default=False)
    events = relationship("Events", back_populates="file_type", cascade="all, delete")


class AttributeTypeList(Base):
    __tablename__ = "AttributeTypeList"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)


class DictionaryList(Base):
    __tablename__ = "DictionaryList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updateDate"
    )
    create_user = Column(String, name="createUser", nullable=True)
    update_user = Column(String, name="updateUser", nullable=True)
    dictionary_value_list = relationship(
        "DictionaryValueList", back_populates="dictionary_list", cascade="all, delete"
    )


class DictionaryValueList(Base):
    __tablename__ = "DictionaryValueList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updateDate"
    )
    create_user = Column(String, name="createUser", nullable=True)
    update_user = Column(String, name="updateUser", nullable=True)
    dictionary_id = Column(
        Integer,
        ForeignKey("DictionaryList.id", ondelete="CASCADE"),
        name="dictionaryId",
    )
    dictionary_list = relationship(
        "DictionaryList", back_populates="dictionary_value_list"
    )
    dictionary_code = Column(
        String, name="dictionarycode"
    )  # TODO исправить на camel case когда Никита перейдет на асинк
    parent_id = Column(
        Integer, name="parentid"
    )  # TODO исправить на camel case когда Никита перейдет на асинк


class AttributeList(Base):
    __tablename__ = "AttributeList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updateDate"
    )
    create_user = Column(String, name="createUser", nullable=True)
    update_user = Column(String, name="updateUser", nullable=True)
    file_type_to_attribute = relationship(
        "FileType2Attribute", back_populates="attribute_list", cascade="all, delete"
    )
    type_id = Column(
        Integer, ForeignKey("AttributeTypeList.id", ondelete="CASCADE"), name="typeId"
    )
    attribute_type = relationship("AttributeTypeList")
    dictionary_id = Column(
        Integer,
        ForeignKey("DictionaryList.id", ondelete="SET NULL"),
        name="dictionaryId",
    )
    dictionary_list = relationship("DictionaryList")
    rule_filters = relationship("RuleFilters", back_populates="attribute_list")
    event_filters = relationship("EventFilters", back_populates="attribute_list")


class FileType2Attribute(Base):
    __tablename__ = "FileType2Attribute"

    id = Column(Integer, primary_key=True, index=True)
    file_type_id = Column(
        Integer, ForeignKey("FileType.id", ondelete="CASCADE"), name="fileTypeId"
    )
    file_type = relationship("FileType", back_populates="file_type_to_attribute")
    attribute_id = Column(
        Integer, ForeignKey("AttributeList.id", ondelete="CASCADE"), name="attributeId"
    )
    attribute_list = relationship(
        "AttributeList", back_populates="file_type_to_attribute"
    )


class DirectoryList(Base):
    __tablename__ = "DirectoryList"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, name="parentId")
    name = Column(String)
    full_path = Column(String, name="fullPath")
    create_date = Column(DateTime, default=datetime.now, name="createdate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updatedate"
    )
    create_user = Column(String, name="createuser", nullable=True)
    update_user = Column(String, name="updateuser", nullable=True)
    root_list = relationship(
        "RootList", back_populates="directory_list", cascade="all, delete"
    )
    file_list = relationship(
        "FileList", back_populates="directory_list", cascade="all, delete"
    )
    dictionary_code = Column(String, name="nodeTypeCode")
    dictionary_value_code = Column(String, name="nodeTypeValueCode")
    description = Column(String)
    role_to_directory = relationship(
        "Role2Directory", back_populates="directory", cascade="all, delete"
    )

    __table_args__ = (UniqueConstraint("name", "fullPath", name="unique_subdirectory"),)


class RootList(Base):
    __tablename__ = "RootList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    root_directory_id = Column(
        Integer,
        ForeignKey("DirectoryList.id", ondelete="CASCADE"),
        name="rootDirectoryId",
    )
    directory_list = relationship("DirectoryList", back_populates="root_list")
    role_to_root_list = relationship(
        "Role2RootList", back_populates="root_list", cascade="all, delete"
    )


class StatusFileList(Base):
    __tablename__ = "StatusFileList"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    file_list = relationship("FileList", back_populates="status")
    rules = relationship("Rules", back_populates="status_file_list")
    events = relationship("Events", back_populates="status_file_list")


class BucketList(Base):
    __tablename__ = "BucketList"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(Integer)
    code = Column(String)
    file_list = relationship("FileList", back_populates="bucket", cascade="all, delete")


class FileList(Base):
    __tablename__ = "FileList"

    id = Column(BigInteger, primary_key=True, index=True)
    file_type_id = Column(
        Integer, ForeignKey("FileType.id", ondelete="CASCADE"), name="fileTypeId"
    )
    file_type = relationship("FileType", back_populates="file_list")
    fid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    file_name = Column(String, name="fileName")
    file_size = Column(BigInteger, name="fileSize")
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    update_date = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, name="updateDate"
    )
    directory_id = Column(
        Integer, ForeignKey("DirectoryList.id", ondelete="CASCADE"), name="directoryId"
    )
    directory_list = relationship("DirectoryList", back_populates="file_list")
    full_path = Column(String, name="fullPath")
    status_id = Column(
        Integer, ForeignKey("StatusFileList.id", ondelete="CASCADE"), name="statusId"
    )
    status = relationship("StatusFileList", back_populates="file_list")
    bucket_id = Column(
        Integer, ForeignKey("BucketList.id", ondelete="CASCADE"), name="bucketId"
    )
    bucket = relationship("BucketList", back_populates="file_list")
    flag = Column(Integer)
    create_user = Column(String, name="createUser", nullable=True)
    update_user = Column(String, name="updateUser", nullable=True)
    actual_date = Column(DateTime, name="actualDate")
    file_attribute = relationship(
        "FileAttributeValue", back_populates="file", cascade="all, delete"
    )
    file_meta = relationship("FileMeta", back_populates="file", cascade="all, delete")


class FileAttributeValue(Base):
    __tablename__ = "FileAttributeValue"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(
        BigInteger, ForeignKey("FileList.id", ondelete="CASCADE"), name="fileId"
    )
    file = relationship("FileList", back_populates="file_attribute")
    attribute_id = Column(
        Integer, ForeignKey("AttributeList.id", ondelete="CASCADE"), name="attributeId"
    )
    value_str = Column(String, name="valueStr")
    value_code = Column(String, name="valueCode")
    value_date = Column(DateTime, name="valueDate")
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    file_type_id = Column(Integer, name="fileTypeId")
    value_number = Column(Float, name="valueNumber")


class FileMeta(Base):
    __tablename__ = "FileMeta"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(
        BigInteger, ForeignKey("FileList.id", ondelete="CASCADE"), name="fileId"
    )
    file = relationship("FileList", back_populates="file_meta")
    meta = Column(JSONB)


class Rules(Base):
    __tablename__ = "Rules"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    file_type_id = Column(
        Integer, ForeignKey("FileType.id", ondelete="CASCADE"), name="fileTypeId"
    )
    file_type = relationship("FileType", back_populates="rules")
    move_days = Column(Integer, name="moveDays")
    delete_days = Column(Integer, name="deleteDays")
    move_to_3_days = Column(Integer, name="moveTo3Days")
    rule_filters = relationship(
        "RuleFilters", back_populates="rule", cascade="all, delete"
    )
    status_file_id = Column(
        Integer,
        ForeignKey("StatusFileList.id", ondelete="CASCADE"),
        name="statusFileId",
    )
    status_file_list = relationship("StatusFileList", back_populates="rules")


class RuleFilters(Base):
    __tablename__ = "RuleFilters"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("Rules.id", ondelete="CASCADE"), name="ruleId")
    rule = relationship("Rules", back_populates="rule_filters")
    attribute_id = Column(
        Integer, ForeignKey("AttributeList.id", ondelete="CASCADE"), name="attributeId"
    )
    attribute_list = relationship("AttributeList", back_populates="rule_filters")
    value_str = Column(String, name="valueStr")
    value_code = Column(String, name="valueCode")
    value_date = Column(DateTime, name="valueDate")
    value_number = Column(Float, name="valueNumber")


class FileType2DVL(Base):
    __tablename__ = "FileType2DVL"

    id = Column(Integer, primary_key=True, index=True)
    file_type_code = Column(String, name="filetypecode")
    dvl_code = Column(String, name="dvlcode")


class GisProjectsFolders(Base):
    __tablename__ = "GisProjectsFolders"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(UUID)
    create_date = Column(DateTime, default=datetime.now, name="createDate")
    ruid = Column(UUID)


class FtpSetting(Base):
    __tablename__ = "FtpSetting"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    host = Column(String)
    user = Column(String)
    passwd = Column(String)
    acct = Column(String)
    timeout = Column(Float)
    source_address = Column(String)
    encoding = Column(String)


class Role2FileType(Base):
    __tablename__ = "Role2FileType"

    id = Column(Integer, primary_key=True, index=True)
    role_group_id = Column(
        Integer, ForeignKey("RoleGroupList.id", ondelete="CASCADE"), name="roleGroupId"
    )
    role = relationship("RoleGroupList", back_populates="role_to_file_type")
    file_type_id = Column(
        Integer, ForeignKey("FileType.id", ondelete="CASCADE"), name="fileTypeId"
    )
    file_type = relationship("FileType", back_populates="role_to_file_type")


class Role2RootList(Base):
    __tablename__ = "Role2RootList"

    id = Column(Integer, primary_key=True, index=True)
    role_group_id = Column(
        Integer, ForeignKey("RoleGroupList.id", ondelete="CASCADE"), name="roleGroupId"
    )
    role = relationship("RoleGroupList", back_populates="role_to_root_list")
    root_list_id = Column(
        Integer, ForeignKey("RootList.id", ondelete="CASCADE"), name="rootListId"
    )
    root_list = relationship("RootList", back_populates="role_to_root_list")


class Role2DictionaryValue(Base):
    __tablename__ = "Role2DictionaryValue"

    id = Column(Integer, primary_key=True, index=True)
    role_group_id = Column(
        Integer, ForeignKey("RoleGroupList.id", ondelete="CASCADE"), name="roleGroupId"
    )
    role = relationship("RoleGroupList", back_populates="role_to_dictionary")
    dictionary_value_code = Column(String, name="dictionaryValueCode")
    dictionary_code = Column(String, name="dictionaryCode")


class Notification(Base):
    __tablename__ = "Notification"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    message = Column(String)
    send_date = Column(DateTime, name="sendDate")
    read_date = Column(DateTime, name="readDate")
    additional_info = Column(String, name="additionalInfo")
    info_code = Column(String, name="infoCode")
    status_code = Column(String, name="statusCode")
    user_name = Column(String, name="userName")
    task_id = Column(UUID, name="taskId")
    task_id_code = Column(String, name="taskIdCode")


class RelDBSetting(Base):
    __tablename__ = "RelDBSetting"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    db_name = Column(String, name="dbName")
    host = Column(String)
    port = Column(Integer)
    user = Column(String)
    passwd = Column(String)


class NsiValue(Base):
    __tablename__ = "NsiValue"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    version = Column(Integer, name="version", nullable=False)
    content = Column(String, name="content", nullable=False)
    createDate = Column(DateTime, name="createDate", default=datetime.now)
    updateDate = Column(
        DateTime, name="updateDate", default=datetime.now, onupdate=datetime.now
    )
    dictionaryCode = Column(String, name="dictionaryCode", nullable=False)


class ARM2InfoProd(Base):
    __tablename__ = "ARM2InfoProd"

    id = Column(Integer, primary_key=True, index=True)
    arm_code = Column(String, name="armCode")
    info_prod_code = Column(String, name="infoProdCode")


class Role2Directory(Base):
    __tablename__ = "Role2Directory"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(
        Integer, ForeignKey("RoleGroupList.id", ondelete="CASCADE"), name="roleId"
    )
    role = relationship("RoleGroupList", back_populates="role_to_directory")
    directory_id = Column(
        Integer, ForeignKey("DirectoryList.id", ondelete="CASCADE"), name="directoryId"
    )
    directory = relationship("DirectoryList", back_populates="role_to_directory")


class Events(Base):
    __tablename__ = "Events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    event_filters = relationship(
        "EventFilters", back_populates="events", cascade="all, delete"
    )
    file_type_id = Column(
        Integer, ForeignKey("FileType.id", ondelete="CASCADE"), name="fileTypeId"
    )
    file_type = relationship("FileType", back_populates="events")
    request_url = Column(String, name="requestUrl")
    status_file_id = Column(
        Integer,
        ForeignKey("StatusFileList.id", ondelete="CASCADE"),
        name="statusFileId",
    )
    status_file_list = relationship("StatusFileList", back_populates="events")


class EventFilters(Base):
    __tablename__ = "EventFilters"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(
        Integer, ForeignKey("Events.id", ondelete="CASCADE"), name="eventId"
    )
    events = relationship("Events", back_populates="event_filters")
    attribute_id = Column(
        Integer, ForeignKey("AttributeList.id", ondelete="CASCADE"), name="attributeId"
    )
    attribute_list = relationship("AttributeList", back_populates="event_filters")
    value_str = Column(String, name="valueStr")
    value_code = Column(String, name="valueCode")
    value_date = Column(DateTime, name="valueDate")
    value_number = Column(Float, name="valueNumber")


class FormatFiles(Base):
    __tablename__ = "FormatFiles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
