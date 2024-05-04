import time

from pydantic import BaseModel
from typing import List, Optional
from yunxiao import YunXiao, Page


class _CampusDto(BaseModel):
    id: int
    companyId: int
    teacherId: int
    campusId: int
    campusName: str


class _RoleDto(BaseModel):
    companyId: int
    productCode: int
    terminalType: int
    teacherId: int
    roleId: int
    roleParentId: int
    roleName: str
    roleIds: Optional[list]


class _OrgStructure(BaseModel):
    id: int
    orgStructureId: int
    orgStructureName: str
    leaderStatus: int


class Photo(BaseModel):
    ext: Optional[str] = None
    fileKey: Optional[str] = None
    mimeType: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    duration: Optional[int] = None
    bucket: Optional[str] = None
    fileSize: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    name: Optional[str] = None
    etag: Optional[str] = None
    fileId: Optional[str] = None


class Teacher(BaseModel):
    id: int
    name: str
    phone: str
    sex: int
    photo: Photo
    superAdmin: bool
    admin: Optional[bool]
    activation: bool
    companyId: int
    companyName: Optional[str]
    roleIds: Optional[List[int]]
    campusIds: Optional[List[int]]
    roleList: list
    campusList: Optional[list]
    teacherCampusDtos: Optional[List[_CampusDto]]
    teacherRoleDtos: Optional[List[_RoleDto]]
    orgStructureList: Optional[List[_OrgStructure]]
    dataRole: int
    status: int
    leaveOffInfo: Optional[str]
    activated: bool


class Teschers(BaseModel):
    data: List[Teacher] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class TeschersQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []
        queryKey: str = ""
        roleIds: List[int] = []
        statusIds: List[int] = []
        _t_: int = int(time.time() * 1000)
        page: Page = Page(pageNum=1, pageSize=100)
    """
    campusIds: List[int] = []
    queryKey: str = ""
    roleIds: List[int] = []
    statusIds: List[int] = []
    _t_: int = int(time.time() * 1000)
    page: Page = Page()


def query_teachers(auth: YunXiao, payload: TeschersQueryPayload) -> Teschers:
    endpoint = f"https://{auth.host}/api/cs-pc-crm/teacher/pageList"
    result_type = Teschers
    return auth.pages_looper(endpoint, payload, result_type)
