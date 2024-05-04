import time

from pydantic import BaseModel, field_validator
from typing import List, Optional, Union
from decimal import Decimal
from datetime import datetime
from yunxiao import YunXiao, Page


# 账户


class TradeAccount(BaseModel):
    id: int
    name: str

    class Config:
        extra = "allow"


class TradeAccounts(BaseModel):
    data: Optional[List[TradeAccount]] = []
    currentTimeMillis: int = None
    code: int = None
    msg: str = ""
    page: Page = Page()


class TradeAccountsQueryPayload(BaseModel):
    """
    Attributes:
        status: List[int] = []  # 状态：0-停用 1-启用
    """
    status: int = 1  # 状态：0-停用 1-启用
    page: Page = Page(pageSize=999)
    _t_: int = int(time.time() * 1000)


def query_accounts(auth: YunXiao, payload: TradeAccountsQueryPayload) -> TradeAccounts:
    endpoint = f"https://{auth.host}/api/cs-pc-edu/paymentAccount/customPage"
    result_type = TradeAccounts
    return auth.pages_looper(endpoint, payload, result_type)


# 收款


class RevenueRecord(BaseModel):
    orderId: int
    groupId: int
    groupNo: str
    campusId: int
    campusName: str
    studentId: int
    studentName: str
    buyerNameStr: str
    phone: str
    relation: Optional[str]
    orderType: int
    orderStatus: int
    orderTypeDesc: str
    orderStatusDesc: str
    payFact: Decimal
    walletMoney: Decimal
    onlineMoney: Decimal
    offlineMoney: Decimal
    storedCardMoney: Decimal
    storedCardPrincipalMoney: Decimal
    storedCardGiveMoney: Decimal
    payTypeDesc: str
    payTime: datetime
    paymentAccountCustoms: Optional[List[TradeAccount]]
    payTimeStr: str
    handleTeacherId: int
    handleTeacherName: str
    orderNo: str
    payStatus: Optional[int]
    orderTime: datetime
    sourceType: int
    sourceTypeStr: str
    confirmStatus: int
    confirmOperaId: Optional[int]
    confirmOperaName: Optional[str]
    confirmTime: Optional[datetime]
    btransactionId: Optional[int]

    @field_validator('payTime', 'orderTime', 'confirmTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class _RevenueRecordsDetail(BaseModel):
    paymentDetailDtos: List[RevenueRecord] = []
    totalPayFact: Decimal
    totalWalletMoney: Decimal
    totalOnlineMoney: Decimal
    totalOfflineMoney: Decimal
    totalStoredCardMoney: Decimal
    totalStoredCardPrincipalMoney: Decimal
    totalStoredCardGiveMoney: Decimal


class RevenueRecords(BaseModel):
    data: Optional[List[RevenueRecord]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        return _RevenueRecordsDetail(**v).paymentDetailDtos


class RevenueRecordsQueryPayload(BaseModel):
    """
    Attributes:
        payStartTime: str = ""  # 支付时间-起始
        payEndTime: str = ""  # 支付时间-结束
        orderStartTime: str = ""  # 订单创建时间-起始
        orderEndTime: str = ""  # 订单创建时间-结束
        campusIds: List[int] = []  # 校区
        groupNo: str = ""  # 收据编号
        orderNo: str = ""  # 关联订单编号
        handleTeacherId: Optional[int]  # 操作人
        confirmStatusList: List[int] = []  # 入账状态：1-待确认 2-已确认
        revenueType: int = ""  # 收入类型：0-收费 1-转课
        orderStatus: int = ""  # 订单状态：1-已付款 2-已作废
        payType: int = ""  # 支付方式：0-钱包支付 1-线上支付 2-线下收款 3-储值卡支付
        studentIds: List[int] = []  # 学员
        phone: str = ""  # 手机号码
        paymentAccountCustomIds: List[int] = []  # 收款账户
        cardName: str = ""  # 持卡人
        btransactionId: str = ""  # 支付单号
    """
    campusIds: List[int] = []  # 校区
    payStartTime: str = ""  # 支付时间-起始
    payEndTime: str = ""  # 支付时间-结束
    orderStartTime: str = ""  # 订单创建时间-起始
    orderEndTime: str = ""  # 订单创建时间-结束
    btransactionId: str = ""  # 支付单号
    cardName: str = ""  # 持卡人
    confirmStatusList: List[int] = []  # 入账状态：1-待确认 2-已确认
    groupNo: str = ""  # 收据编号
    handleTeacherId: Optional[int] = None
    orderNo: str = ""  # 关联订单编号
    orderStatus: int = None  # 订单状态：1-已付款 2-已作废
    page: Page = Page()
    payType: int = None  # 支付方式：0-钱包支付 1-线上支付 2-线下收款 3-储值卡支付
    paymentAccountCustomIds: List[int] = []  # 收款账户
    phone: str = ""  # 手机号码
    revenueType: int = None  # 收入类型：0-收费 1-转课
    studentIds: List[int] = []  # 学员
    _t_: int = int(time.time() * 1000)


# 退款


class RefundRecord(BaseModel):
    companyId: int
    campusId: int
    campusName: str
    studentId: int
    studentName: str
    buyerNameStr: str
    orderNo: Optional[str]
    refundOrderNo: str
    sourceType: Optional[int]
    refundOrderStatus: Optional[int]
    remark: Optional[str]
    refundMoney: Optional[Decimal]
    refundFreeMoney: Decimal
    realRefundMoney: Decimal
    operatorId: int
    operatorName: str
    refundApplyId: Optional[int]
    refundOrderId: Optional[int]
    originalOrderId: Optional[int]
    paymentAccountId: Optional[int]
    refundTime: datetime
    createTime: datetime
    refundFinishTime: datetime
    ztRefundId: Optional[int]
    refundType: Optional[str]
    refundMethod: Optional[int]
    phone: str
    relation: Optional[str]
    confirmStatus: int
    confirmOperaId: Optional[int]
    confirmOperaName: Optional[str]
    confirmTime: Optional[datetime]
    paymentAccountCustoms: Optional[List[TradeAccount]]

    @field_validator('refundTime', 'createTime', 'refundFinishTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class RefundRecords(BaseModel):
    data: Optional[List[RefundRecord]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        class _RefundRecordsDetail(BaseModel):
            paymentRefundDtos: List[RefundRecord] = []
            totalRefundMoney: Decimal
        return _RefundRecordsDetail(**v).paymentRefundDtos


class RefundRecordsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        refundFinishStartTime: str = ""  # 退款时间-起始
        refundFinishEndTime: str = ""  # 退款时间-结束
        orderNo: str = ""  # 退费订单编号
        refundMethodList: List[int] = []  # 退款方式：1-线上退款 2-线下退款
        phone: str = ""  # 手机号码
        studentIds: List[int] = []  # 学员
        paymentAccountCustomIds: List[int] = []  # 退款账户
        confirmStatusList: List[int] = []  # 出账状态：1-待确认 2-已确认
        handleTeacherId: Optional[int] = None  # 操作人
        cardName: str = ""  # 持卡人
    """
    campusIds: List[int] = []  # 校区
    cardName: str = ""  # 持卡人
    confirmStatusList: List[int] = []  # 出账状态：1-待确认 2-已确认
    handleTeacherId: Optional[int] = None  # 操作人
    orderNo: str = ""  # 退费订单编号
    paymentAccountCustomIds: List[int] = []  # 退款账户
    phone: str = ""  # 手机号码
    refundFinishStartTime: str = ""  # 退款时间-起始
    refundFinishEndTime: str = ""  # 退款时间-结束
    refundMethodList: List[int] = []  # 退款方式：1-线上退款 2-线下退款
    studentIds: List[int] = []  # 学员
    page: Page = Page()
    _t_: int = int(time.time() * 1000)


# 账户交易记录


class AccountRecord(BaseModel):
    id: int
    companyId: int
    campusId: int
    campusName: str
    operatorId: int
    operatorName: str
    isSelf: bool
    operatorTime: datetime
    orderId: Optional[int]
    paymentGroupId: Optional[int]
    paymentRecordId: Optional[int]
    orderNo: Optional[str]
    money: Decimal
    paymentAccountCustomId: Optional[int]
    paymentAccountCustomName: Optional[str]
    type: int
    typeName: str
    recordType: int
    studentId: int
    studentName: str
    buyerNameStr: str
    parentPhone: str
    phone: Optional[str]
    relation: Optional[str]
    parentShowText: Optional[str]

    @field_validator('operatorTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class AccountRecords(BaseModel):
    data: Optional[List[AccountRecord]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class AccountRecordsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        displayInvalidOrder: bool = False  # 是否展示已作废订单
        startTime: str = ""  # 操作时间-起始
        endTime: str = ""  # 操作时间-结束
        paymentAccountCustomIds: List[int] = []  # 账户
        typeList: List[int] = []  # 收支类型：0-收费 1-转课 2-退费
    """
    campusIds: List[int] = []  # 校区
    displayInvalidOrder: bool = False  # 是否展示已作废订单
    startTime: str = ""  # 操作时间-起始
    endTime: str = ""  # 操作时间-结束
    paymentAccountCustomIds: List[int] = []  # 账户
    typeList: List[int] = []  # 收支类型：0-收费 1-转课 2-退费
    page: Page = Page()
    _t_: int = int(time.time() * 1000)


def query_records(
        auth: YunXiao,
        payload: Union[RevenueRecordsQueryPayload, RefundRecordsQueryPayload, AccountRecordsQueryPayload]
) -> Union[RevenueRecords, RefundRecords, AccountRecords]:
    if isinstance(payload, RevenueRecordsQueryPayload):
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findPaymentList"
        result_type = RevenueRecords
    elif isinstance(payload, RefundRecordsQueryPayload):
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findPaymentRefundList"
        result_type = RefundRecords
    else:
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findPaymentAccountCustomRecord"
        result_type = AccountRecords
    return auth.pages_looper(endpoint, payload, result_type)
