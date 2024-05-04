from pydantic import BaseModel, field_validator, computed_field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid
import time
from yunxiao import YunXiao, Page


class Achievement(BaseModel):
    processDate: datetime
    campusName: str
    orderNo: str
    studentId: int
    studentName: str
    comeFromDesc: str
    orderType: str
    orderFlagName: str
    productType: str
    productName: str
    totalMoney: Decimal
    teacherName: str
    scaleStr: str
    scaleMoney: Decimal

    @computed_field
    def id(self) -> str:
        return str(uuid.uuid4())

    @field_validator('totalMoney', 'scaleMoney', mode='before')
    def validate_money(cls, v: str):
        return Decimal(v.replace(",", "")) if v else 0

    @field_validator('processDate', mode='before')
    def validate_processDate(cls, v: str):
        return datetime.strptime(v, '%Y-%m-%d  %H:%M') if ':' in v else datetime.strptime(v, '%Y-%m-%d')


class _Data(BaseModel):
    achievementBelongerDetailItems: Optional[List[Achievement]] = []
    tscaleMoney: str
    ttotalMoney: str


class Achievements(BaseModel):
    data: Optional[List[Achievement]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        return _Data(**v).achievementBelongerDetailItems


class AchievementsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []
        startDate: str
        endDate: str
        orderNo: str = ""
        orderTypes: List[int] = [] 订单类型：0-收费 2-退费 3-结转
        orderFlagIds: List[int] = []
        productName: str = "" 项目名称
        productTypes: List[int] 订单项目：0-物品 1-课程 2-班级 4-课时包
        studentId: str = ""
        teacherIds: List[int] = []
        _t_: int = int(time.time() * 1000)
        page: Page = Page(pageNum=1, pageSize=100)
    """
    campusIds: List[int] = []
    startDate: str
    endDate: str
    orderNo: str = ""
    orderTypes: List[int] = []
    orderFlagIds: List[int] = []
    productName: str = ""
    productTypes: List[int] = []
    studentId: str = ""
    teacherIds: List[int] = []
    _t_: int = int(time.time() * 1000)
    page: Page = Page()


def query_records(auth: YunXiao, payload: AchievementsQueryPayload) -> Achievements:
    endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findAchievementBelongerDetail"
    result_type = Achievements
    return auth.pages_looper(endpoint, payload, result_type)
