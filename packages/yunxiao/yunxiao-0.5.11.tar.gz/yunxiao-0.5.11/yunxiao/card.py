from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
import time
from yunxiao import YunXiao, Page


class Card(BaseModel):
    cardCourseTradedId: int
    companyId: int
    campusId: int
    campusName: str
    studentId: int
    studentName: str
    parentPhone: str
    curriculumId: int
    curriculumName: str
    cardInfoId: int
    cardInfoName: str
    cardType: int
    chargeType: int
    priceUnitName: str
    feeWarnStatus: int
    buyAmount: Decimal
    freeAmount: Decimal
    totalAmount: Decimal
    consumeAmount: Decimal
    consumeFreeAmount: Decimal
    totalConsumeAmount: Decimal
    refundBuyAmount: Decimal
    refundFreeAmount: Decimal
    totalRefundAmount: Decimal
    transferAmount: Decimal
    transferFreeAmount: Decimal
    totalTransferAmount: Decimal
    totalRefundTransferAmount: Decimal
    expireAmount: Decimal
    expireFreeAmount: Decimal
    totalExpireAmount: Decimal
    remainAmount: Decimal
    remainFreeAmount: Decimal
    totalRemainAmount: Decimal
    totalRemainBuyAmount: Decimal
    totalRemainFreeAmount: Decimal
    totalAvailableRemainAmount: Decimal
    oweAmount: Decimal
    totalMoney: Decimal
    consumeMoney: Decimal
    remainMoney: Decimal
    expireMoney: Decimal
    oweMoney: Decimal


class Cards(BaseModel):
    data: Optional[List[Card]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class CardsQueryPayload(BaseModel):
    _t_: Optional[int] = int(time.time() * 1000)
    page: Page = Page()
    campusIds: List[int] = []  # 校区
    studentClassIds: List[int] = []  # 班级
    studentStatusList: List[int] = []  # 学员状态：0-未收费 1-在读 7-停课
    studentIds: List[int] = []  # 学生
    displayHistory: bool = True  # 曾就读学员：True-展示 False-不展示
    cardType: Optional[int] = None  # 上课卡：None-不限 0-课程 1-课时包
    feeWarnStatus: int = 0  # 上课卡状态：0-不限 1-正常 2-不再费用预警
    curriculumIds: List[int] = []  # 课程
    cardInfoIds: List[int] = []  # 课程卡
    remainAmountMin: Optional[str] = ""  # 最小剩余数量
    remainAmountMax: Optional[str] = ""  # 最大剩余数量
    sort: Optional[str] = None
    sortField: Optional[str] = None


def query_records(auth: YunXiao, payload: CardsQueryPayload) -> Cards:
    endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/studentCourseCard/report"
    result_type = Cards
    return auth.pages_looper(endpoint, payload, result_type)
