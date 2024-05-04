import time

from pydantic import BaseModel, field_validator
from typing import List, Optional, Literal, Union
from decimal import Decimal
from datetime import datetime
from yunxiao import YunXiao, Page


class ConsumeDetail(BaseModel):
    id: Optional[int]
    studentId: Optional[int]
    studentName: Optional[str]
    curriculumId: Optional[int]
    curriculumName: Optional[str]
    classId: Optional[int]
    className: Optional[str]
    courseTime: Optional[datetime]
    chargeId: Optional[int]
    teacherId: Optional[int]
    teacherName: Optional[str]
    assistantTeacherIds: Optional[List[int]]
    assistantTeacherNames: Optional[str]
    consumeAmount: Optional[Decimal]
    courseMoney: Optional[Decimal]
    cardId: Optional[int]
    cardName: Optional[str]
    cardType: Optional[int]
    orderNo: Optional[str]
    orderCreateTime: Optional[datetime]
    orderFirstPaymentTime: Optional[datetime]
    sourceType: Optional[int]
    oweAmount: Optional[Decimal]
    chargeType: Optional[int]
    payMethod: Optional[int]

    @field_validator('courseTime', 'orderCreateTime', 'orderFirstPaymentTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class ConsumeDetails(BaseModel):
    data: Optional[List[ConsumeDetail]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        class data(BaseModel):
            courseConsumeDetailList: List[ConsumeDetail] = []
            totalConsumeMoney: Decimal
            totalConsumeAmount: Decimal
            totalClassConsumeAmount: Decimal
            totalOweAmount: Decimal
            totalClassOweAmount: Decimal
        return data(**v).courseConsumeDetailList


class ConsumeDetailsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        classId: Optional[int] = None  # 班级
        studentIds: List[int] = []  # 学员
        teacherIds: List[int] = []  # 上课老师
        courseStartTime: str = ""  # 上课时间-起始
        courseEndTime: str = ""  # 上课时间-结束
        assistantTeacherIds: List[int] = []  # 助教
        curriculumIds: List[int] = []  # 课程
    """
    _t_: int = int(time.time() * 1000)
    page: Page = Page()
    campusIds: List[int] = []  # 校区
    classId: Optional[int] = None  # 班级
    studentIds: List[int] = []  # 学员
    teacherIds: List[int] = []  # 上课老师
    courseStartTime: str = ""  # 上课时间-起始
    courseEndTime: str = ""  # 上课时间-结束
    assistantTeacherIds: List[int] = []  # 助教
    curriculumIds: List[int] = []  # 课程


class ConsumeRecord(BaseModel):
    id: Optional[int]
    companyId: Optional[int]
    campusId: Optional[int]
    createTime: Optional[datetime]
    updateTime: Optional[datetime]
    deleted: Optional[bool]
    sourceType: Optional[int]
    sourceFlagId: Optional[int]
    priceItemId: Optional[int]
    curriculumId: Optional[int]
    classId: Optional[int]
    classRoomId: Optional[int]
    classRoomName: Optional[str]
    studentId: Optional[int]
    chargeId: Optional[int]
    receiptNo: Optional[str]
    amount: Optional[Decimal]
    price: Optional[Decimal]
    courseMoney: Optional[Decimal]
    remark: Optional[str]
    courseTime: Optional[datetime]
    studentName: Optional[str]
    className: Optional[str]
    arrangeClassId: Optional[int]
    teacherId: Optional[int]
    teacherName: Optional[str]
    assistantTeacherIds: Optional[List[int]]
    assistantTeacherNames: Optional[str]
    oweAmount: Optional[Decimal]
    priceUnitName: Optional[str]
    chargeType: Optional[int]
    curriculumName: Optional[str]
    operationTime: Optional[datetime]
    operatorId: Optional[int]
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    courseContent: Optional[str]
    courseStudentStatus: Optional[int]
    courseStatus: Optional[int]
    courseStudentStatusShow: Optional[str]
    courseTimePeriod: Optional[str]
    operatorName: Optional[str]

    @field_validator('createTime', 'updateTime', 'courseTime', 'operationTime', 'startTime', 'endTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class ConsumeRecords(BaseModel):
    data: Optional[List[ConsumeRecord]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        class data(BaseModel):
            courseConsumeList: List[ConsumeRecord] = []
            totalConsumeMoney: Decimal
            totalConsumeAmount: Decimal
            totalOweAmount: Decimal
        return data(**v).courseConsumeList


class ConsumeRecordsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        classId: Optional[int] = None  # 班级
        studentIds: List[int] = []  # 学员
        teacherIds: List[int] = []  # 上课老师
        operationStartTime: str = ""  # 操作时间-起始
        operationEndTime: str = ""  # 操作时间-结束
        courseStartTime: str = ""  # 上课时间-起始
        courseEndTime: str = ""  # 上课时间-结束
        sourceTypeList: List[int] = []  # 课消类型：0-点名课消 1-标记补课 2-点名课消（补课） 3-按天自动计费 4-记课消
        courseStudentStatusList: List[int] = []  # 出勤状态：1-出勤 2-迟到 3-请假 4-未到
        assistantTeacherIds: List[int] = []  # 助教
        operatorId: Optional[int] = None  # 操作人
        sort: Literal[0, 1] = 0  # 排序：0-DESC 1-ASC
        sortField: Literal["operationTime", "courseTimePeriod", None]  # 排序字段：operationTime-操作时间 courseTimePeriod-上课时间
        curriculumIds: List[int] = []  # 课程
    """
    _t_: int = int(time.time() * 1000)
    page: Page = Page()
    campusIds: List[int] = []  # 校区
    classId: Optional[int] = None  # 班级
    studentIds: List[int] = []  # 学员
    teacherIds: List[int] = []  # 上课老师
    operationStartTime: str = ""  # 操作时间-起始
    operationEndTime: str = ""  # 操作时间-结束
    courseStartTime: str = ""  # 上课时间-起始
    courseEndTime: str = ""  # 上课时间-结束
    sourceTypeList: List[int] = []  # 课消类型：0-点名课消 1-标记补课 2-点名课消（补课） 3-按天自动计费 4-记课消
    courseStudentStatusList: List[int] = []  # 出勤状态：1-出勤 2-迟到 3-请假 4-未到
    assistantTeacherIds: List[int] = []  # 助教
    operatorId: Optional[int] = None  # 操作人
    sort: Literal[0, 1] = 1  # 排序：0-ASC 1-DESC
    sortField: Literal["operationTime", "courseTimePeriod", None] = "courseTimePeriod"  # 排序字段
    curriculumIds: List[int] = []  # 课程


def query_records(
        auth: YunXiao,
        payload: Union[ConsumeRecordsQueryPayload, ConsumeDetailsQueryPayload]
) -> Union[ConsumeRecords, ConsumeDetails]:
    if isinstance(payload, ConsumeRecordsQueryPayload):
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findCourseSignCharge"
        result_type = ConsumeRecords
    else:
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findCourseSignChargeDetail"
        result_type = ConsumeDetails
    return auth.pages_looper(endpoint, payload, result_type)
