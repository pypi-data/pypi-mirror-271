from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import time
from yunxiao import YunXiao, Page


class OrderItem(BaseModel):
    class _businessJson(BaseModel):
        class _priceItemDetail(BaseModel):
            priceUnit: Optional[str] = None
            originalPrice: Optional[int] = None
            priceNum: Optional[Decimal] = None
            campusId: Optional[int] = None
            priceTypeName: Optional[str] = None
            chargeType: Optional[int] = None
            priceItemDetailId: Optional[int] = None
            priceType: Optional[int] = None
            commodityId: Optional[int] = None
            priceItemName: Optional[str] = None
            priceUnitName: Optional[str] = None
            classId: Optional[int] = None
            commodityPriceType: Optional[int] = None
            companyId: Optional[int] = None
            price: Optional[Decimal] = None
            priceItemId: Optional[int] = None
            id: Optional[int] = None
            priceName: Optional[str] = None
            status: Optional[bool] = None

        class _chargeRule(BaseModel):
            chargeType: Optional[int] = None

        class _achievementBelonger(BaseModel):
            scaleStr: str
            teacherId: int
            scale: int
            id: int

        class _priceDimension(BaseModel):
            companyId: int
            id: int
            dimensionName: str
            dimensionValue: str
            curriculumId: int
            basePriceDimensionId: int
            basePriceDimensionDetailId: int

        priceItemDetail: Optional[_priceItemDetail] = None
        chargeRule: Optional[_chargeRule] = None
        achievementBelongerList: Optional[List[_achievementBelonger]] = None
        validInClassDate: int = None
        priceDimensionList: Optional[List[_priceDimension]] = None

    companyId: int
    campusId: int
    campusName: str
    studentId: int
    studentName: str
    phone: str
    productName: str
    productType: int
    productTypeStr: str
    orderFlagId: Optional[int]
    orderFlagName: Optional[str]
    businessJson: Optional[_businessJson]
    priceDetail: Optional[str]
    priceDetailStr: Optional[str]
    courseAmount: Optional[str]
    productQuantity: Optional[str]
    freeAmount: Optional[str]
    discountMoneyStr: Optional[str]
    refundIncomeMoneyStr: Optional[str]
    refundDeductPayMoneyStr: Optional[str]
    receivableMoneyStr: Optional[str]
    totalMoneyStr: Optional[str]
    transferInMoneyStr: Optional[str]
    realMoney: Optional[Decimal]
    oweMoneyStr: Optional[str]
    sourceType: Optional[int]
    sourceTypeStr: Optional[str]
    orderType: Optional[int]
    orderTypeStr: Optional[str]
    orderStatusAll: Optional[int]
    orderStatusStr: Optional[str]
    orderNo: Optional[str]
    originalOrderNo: Optional[str]
    createTime: datetime
    creatorId: int
    creatorName: str
    orderId: int
    orderItemId: int
    tableType: int
    achievementBelongerStr: Optional[str]
    priceUnitName: Optional[str]
    comeFrom: Optional[str]
    orderNotes: Optional[str]
    buyerNotes: Optional[str]
    refundRemark: Optional[str]
    buyerName: Optional[str]
    buyerNameStr: Optional[str]
    discountMoney: Optional[Decimal]
    promotionMoney: Optional[Decimal]
    promotionMoneyStr: Optional[Decimal]
    originalPrice: Optional[Decimal]
    totalAndPromotionMoney: Optional[Decimal]
    totalAndPromotionMoneyStr: Optional[Decimal]

    @field_validator('createTime', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None

    @field_validator('realMoney', mode='before')
    def validate_money(cls, v: str):
        return Decimal(v.replace(",", "")) if v else 0


class OrderItems(BaseModel):
    data: Optional[List[OrderItem]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        class _OrderItems(BaseModel):
            orderItemAllList: Optional[List[OrderItem]] = []

        return _OrderItems(**v).orderItemAllList


class OrderItemsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        cardName: str = ""  # 持卡人
        comeFroms: List[int] = []  # 招生来源
        creatorIds: List[int] = []  # 创建人
        startTime: str = ""  # 订单创建时间-起始
        endTime: str = ""  # 订单创建时间-结束
        orderFlagIds: List[int] = []  # 收费类型
        orderNo: str = ""  # 订单编号
        orderStatusAllList: List[int] = []  # 订单状态：0-待付款 1-已付款 2-已取消 3-已失效 4-已作废 6-已退费 7-已结转
        orderTypeAllList: List[int] = []  # 订单类型：0-收费 1-转课 2-退费 3-结转
        oweStatus: int = None  # 欠费状态：0-无欠费 1-有欠费
        phone: str = ""  # 手机号码
        productName: str = ""  # 项目名称
        productTypeList: List[int] = []  # 项目类型：0-物品 1-班级 2-课程 3-电子钱包 4-课时包 5-储值卡
        studentIds: List[int] = []  # 学员
    """
    campusIds: List[int] = []  # 校区
    cardName: str = ""  # 持卡人
    comeFroms: List[int] = []  # 招生来源
    creatorIds: List[int] = []  # 创建人
    startTime: str = ""  # 订单创建时间-起始
    endTime: str = ""  # 订单创建时间-结束
    orderFlagIds: List[int] = []  # 收费类型
    orderNo: str = ""  # 订单编号
    orderStatusAllList: List[int] = []  # 订单状态：0-待付款 1-已付款 2-已取消 3-已失效 4-已作废 6-已退费 7-已结转
    orderTypeAllList: List[int] = []  # 订单类型：0-收费 1-转课 2-退费 3-结转
    oweStatus: Optional[int] = None  # 欠费状态：0-无欠费 1-有欠费
    page: Page = Page()
    phone: str = ""  # 手机号码
    productName: str = ""  # 项目名称
    productTypeList: List[int] = []  # 项目类型：0-物品 1-班级 2-课程 3-电子钱包 4-课时包 5-储值卡
    studentIds: List[int] = []  # 学员
    _t_: int = int(time.time() * 1000)


def query_records(auth: YunXiao, payload: OrderItemsQueryPayload) -> OrderItems:
    endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/findOrderItemAll/page"
    result_type = OrderItems
    return auth.pages_looper(endpoint, payload, result_type)
