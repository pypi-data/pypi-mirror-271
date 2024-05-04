import logging
import time
import requests


def timestamp():
    return int(time.time() * 1000)


class YunXiao:

    def __init__(self, user, pwd, campus: tuple = ()):
        self.host = 'clouds.xiaogj.com'
        self.session = requests.Session()
        self.user, self.pwd = user, pwd
        self.headers = self.renew_auth()
        self.campus = list(campus)

    def renew_auth(self):
        """
        刷新 token.tmp 配置中存储的 token
        """
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                   "Origin": F"https://{self.host}",
                   "Yunxiao-Version": "3.51"}
        self.session.headers.update(headers)

        applogin = self.session.post(
            url=f"https://{self.host}/api/cs-crm/teacher/loginByPhonePwd",
            json={"_t_": timestamp(), "password": self.pwd, "phone": self.user, "userType": 1}
        ).json()["data"]["token"]

        headers["x3-authentication"] = self.session.get(
            url=f"https://{self.host}/api/cs-crm/teacher/businessLogin",
            headers={"x3-authentication": applogin},
            params={"_t_": timestamp()}
        ).json()["data"]["token"]

        # 刷新 cookie

        weblogin = self.session.post(
            url="https://clouds.xiaogj.com/api/ua/login/password",
            params={"productCode": 1, "terminalType": 2, "userType": 1, "channel": "undefined"},
            json={"_t_": timestamp(), "clientId": "x3_prd", "password": self.pwd, "username": self.user,
                  "redirectUri": f"https://{self.host}/web/teacher/#/home/0",
                  "errUri": f"https://{self.host}/web/simple/#/login-error"},
            allow_redirects=False
        )

        weboauth2 = self.session.get(url=weblogin.json()["data"], allow_redirects=False)
        webcode = self.session.get(url=weboauth2.headers["location"], allow_redirects=False)
        webtoken = self.session.get(url=webcode.headers["location"], allow_redirects=False)

        headers["Cookie"] = (f'UASESSIONID={weblogin.cookies.get("UASESSIONID")}; '
                             f'SCSESSIONID={webtoken.cookies.get("SCSESSIONID")}')
        logging.info("登录成功")
        return headers

    def request(self, **kwargs) -> dict:
        response = self.session.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                        params=kwargs.get("params"), headers=self.headers)

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        r_json = response.json()

        if r_json.get("code") == 401:
            logging.error(r_json.get("msg", '未知问题，尝试重新登录。'))
            self.headers = self.renew_auth()
            response = requests.request(method=kwargs.get("method"), url=kwargs.get("url"), json=kwargs.get("json"),
                                        params=kwargs.get("params"), headers=self.headers)

        return response.json()

    # 翻页工具
    @staticmethod
    def loop_pages(key=None):
        """
        :param key: 实际数据所在的字段名
        :return:
        """

        def wrapper_func(func):
            def wrapper(*args, **kwargs) -> list:
                data_list = []  # 结果列表
                page = 1  # 设置起始页为 1
                size = kwargs.get("size")  # 设置每页数量为用户设置的数量

                page_count = 1  # 先假设总页数为 1
                while page <= page_count:  # 列表中数据行的数量不等于 1 时
                    kwargs["page"] = page
                    res = func(*args, **kwargs)
                    try:
                        data = res["data"][key] if key else res["data"]
                        data_list.extend(data)
                    except TypeError:
                        logging.error(res)

                    row_count = res["page"]["totalCount"]  # 取得实际的总行数
                    page_count = res["page"]["totalPage"]  # 取得实际的总页数
                    logging.debug(f"size: {size}, page: {page}/{page_count}, {page * size}/{row_count}")  # 汇报数量
                    page += 1  # 翻页
                return data_list

            return wrapper

        return wrapper_func

    def pages_looper(self, endpoint, payload, schemas):
        response = schemas()  # 结果列表
        response.page.pageSize = payload.page.pageSize
        while payload.page.pageNum <= response.page.totalPage:
            res = self.request(method="post", url=endpoint, json=payload.model_dump())
            try:
                new = schemas(**res)
                response.data.extend(new.data)
                response.page = new.page

                logging.info(
                    f"\033[32m size \033[36m{payload.page.pageSize}"
                    f"\033[32m page \033[36m{response.page.pageNum}/{response.page.totalPage}"
                    f"\033[32m count \033[36m{response.page.pageNum * payload.page.pageSize}/{response.page.totalCount}"
                    f"\033[0m\t{endpoint}"
                )  # 汇报数量

                payload.page.pageNum += 1  # 翻页
            except TypeError:
                logging.error(res)
        response.page.pageSize = payload.page.pageSize
        return response

    # 查询机构指定日期范围业绩。
    def company_query_performance(self, startdate: str, enddate: str) -> list:
        """
        查询机构指定日期范围业绩。
        :param startdate: 起始日期
        :param enddate: 截止日期
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": startdate,
                "endDate": enddate,
                "orderByCampus": 1,
                "_t_": timestamp()
            }
        )["data"]

    # 查询校区（APP接口）
    def campus_query(self) -> list:
        """
        查询全部校区
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/campus/list?type=2"
        )["data"]

    # 查询指定日期范围业绩（APP接口）
    def campus_query_performance(self, start, end: str) -> list:
        """
        分校区列出指定日期的费用数据。
        :param start:
        :param end:
        :return:
        """
        data = self.request(
            method="post",
            url=f"https://{self.host}/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": start,
                "endDate": end,
                "orderByCampus": 1,
                "_t_": timestamp()
            }
        )["data"]
        data_list: list = data["dataReportVos"]
        data_list.append(
            {
                "campusId": 00000000,
                "campusName": "总计",
                "tuitionRevenue": data['totalTuitionRevenue'],
                "dayIncome": 0,
                "courseMoney": data['totalCourseMoney'],
                "courseStudentSize": 0,
                "newStudent": data['totalNewStudent'],
                "date": None,
                "dateStr": None,
                "refundMoney": data['totalRefundMoney'],
                "refundStudentSize": 0,
                "walletMoney": data['totalWalletMoney']
            }
        )
        return data_list

    # 查询意向（APP接口）
    @loop_pages()
    def intentions_query(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                         nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                         startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-crm/intention/clue/allPage",
            json={
                "_t_": timestamp(),
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "status": [0],
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询意向学员（APP接口）
    @loop_pages()
    def intentions_query_students(self, page, size, distributeStatus: int = 1, keyWord: str = "", level: int = "",
                                  nonFollowUpDays: int = "", startNextTime: str = "", endNextTime: str = "",
                                  startLastCommunicateTime: str = "", endLastCommunicateTime: str = ""):
        """
        查询意向学员
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码
        :param distributeStatus: 是否分配跟进人。 **0** 无跟进人 **1** 有跟进人
        :param level: 意向级别。 1-5
        :param keyWord: 查询关键字
        :param nonFollowUpDays: 未跟进天数
        :param startNextTime: 计划跟进时间（查询起点）
        :param endNextTime: 计划跟进时间（查询终点）
        :param startLastCommunicateTime: 最近跟进时间（查询起点）
        :param endLastCommunicateTime: 最近跟进时间（查询终点）
        :return:https://clouds.xiaogj.com/app/teacher/#/cluedetails?id=7127357
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-crm/student/listForIntentionManage",
            json={
                "_t_": timestamp(),
                "distributeStatus": distributeStatus,
                "campusIds": self.campus,
                "keyWord": keyWord,
                "nonFollowUpDays": nonFollowUpDays,
                "level": level,
                "startNextTime": startNextTime,
                "endNextTime": endNextTime,
                "startLastCommunicateTime": startLastCommunicateTime,
                "endLastCommunicateTime": endLastCommunicateTime,
                "page": {"pageNum": page, "pageSize": size}
            }
        )

    # 查询学生
    @loop_pages()
    def students_query(self, page, size, curriculumids: tuple = (), classids: tuple = (), student_ids: tuple = (),
                       status: tuple = (1, 6, 7), class_student_status: int = 0, has_follow_teacher: int = None,
                       start_create_time: str = "", end_create_time: str = ""):
        """
        查询学生
        :param size: 分页查询，每页数量
        :param page: 分页查询，初始页码，应设为 0
        :param curriculumids: 课程筛选
        :param classids: 班级筛选
        :param student_ids: 查询学生
        :param status: 学员状态。 **0** 未收费 **1** 在读 **6** 曾就读 **7** 停课 **99** 无效学员
        :param class_student_status: **0** 不筛选 **1** 未入班 **2** 已入班
        :param has_follow_teacher: **0** 无跟进人 **1** 有跟进人
        :param start_create_time: 起始创建时间
        :param end_create_time: 截止创建时间
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-crm/student/extendList",
            json={
                "_t_": timestamp(),
                "campusIds": self.campus,
                "classIds": list(classids),
                "classStudentStatus": class_student_status,
                "curriculumIds": list(curriculumids),
                "customComeFromIds": [],
                "customGradeIds": [],
                "customFieldValueQueryDtoList": [],
                "startCreateTime": start_create_time,
                "endCreateTime": end_create_time,
                "followTeacherIdsMap": {"1": [], "2": []},
                "introducerIds": [],
                "hasFollowTeacher": has_follow_teacher,
                "onlyQueryRegisterCampus": False,
                "page": {"pageNum": page, "pageSize": size, "count": True},
                "sexList": [],
                "statusList": list(status),
                "studentIds": list(student_ids)
            }
        )

    # 查询学生基本信息
    def student_query_info(self, student_id: int):
        """
        查询学生基本信息
        :param student_id: 学员ID
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-pc-crm/student/detail",
            params={
                "_t_": timestamp(),
                "id": student_id,
                "queryMember": True,
                "queryWallet": True
            }
        )["data"]

    # 查询学生课程卡包
    def student_query_cards(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/studentCard/list",
            json={
                "_t_": timestamp(),
                "studentId": studentid
            }
        )["data"]

    # 查询学生就读课程
    def student_query_course(self, studentid: int) -> list:
        """
        查看学员的课程卡包
        :param studentid: 学生ID
        :return: json数据
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/courseStudent/findStudentAttendCourse",
            json={
                "_t_": timestamp(),
                "studentId": studentid,
                "page": {"pageNum": 1, "pageSize": 1000}
            }
        )["data"]["studentAttendCourseList"]

    # 设置在读学生状态为曾就读
    def student_operation_become_history(self, studentlist: tuple):
        """
        设置学生为曾就读。
        :param studentlist: 学生ID
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/student/becomeHistory",
            json={"_t_": timestamp(), "studentIds": list(studentlist)}
        )

    # 设置曾就读学生状态为在读
    def student_operation_become_study(self, studentlist: tuple):
        """
        设置学生为曾就读。
        :param studentlist: 学生ID
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/student/becomeStudy",
            json={"_t_": timestamp(), "studentIds": list(studentlist)}
        )

    # 查询课程
    @loop_pages()
    def curriculums_query(self, page: int, size: int, searchname: str = None):
        """
        查询课程
        :param page:
        :param size:
        :param searchname: 查找课程名
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/curriculum/page",
            json={
                "_t_": timestamp(),
                "page": {"pageNum": page, "pageSize": size},
                "curriculumName": searchname,
                "dimensionDetailIdList": []
            }
        )

    # 查排课
    @loop_pages()
    def arranges_query(self, page, size, starttime: str, endtime: str, classid: int = "", teacherids: tuple = (),
                       studentids: tuple = (), display_completed_class: bool = False, courseStatusList: tuple = (0, 1)):
        """
        查询某日到某日的排课。
        :param classid: 班级
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param studentids: 查询的学生列表
        :param teacherids: 查询的教师列表
        :param display_completed_class: 是否已结班排课
        :param courseStatusList: 排课状态。 **0** 未点名 **1** 已点名 **2** 已取消
        :param starttime: 查询起始时间 **2020-02-20**
        :param endtime: 查询截止时间 **2020-03-20**
        :return:
        """

        data = {
            "_t_": timestamp(),
            "page": {"pageNum": page, "pageSize": size},
            "campusIds": self.campus,
            "startDate": starttime,
            "endDate": endtime,
            "curriculumIds": [],
            "teacherIds": list(teacherids),
            "assistantTeacherIds": [],
            "classRoomIds": [],
            "studentIds": list(studentids),
            "reserve": 0,
            "displayCompletedClass": display_completed_class,
            "courseStatusList": list(courseStatusList),
            "sortType": 1
        }

        if classid:
            data["classId"] = classid
            data["sortType"] = 2

        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/arrange/page",
            json=data
        )

    # 查询班级
    @loop_pages()
    def classes_query(self, page, size, teacherids: tuple = (), class_ids: tuple = (), class_status: tuple = ()):
        """
        查询班级
        :param size: 分页查询，每页数量
        :param page: 分页查询，起始页码
        :param class_ids: 班级ID
        :param class_status: 班级状态。 **0** 未结班 **1** 已结班
        :param teacherids: 老师ID
        :return:
        """
        return self.request(
            method="post",
            url=f"https://{self.host}/api/cs-pc-edu/classInfo/page",
            json={
                "_t_": timestamp(),
                "queryClassTime": 1,
                "campusIds": self.campus,
                "classIds": list(class_ids),
                "curriculumIds": [],
                "assistantIds": [],
                "page": {"pageNum": page, "pageSize": size, "count": True},
                "classStatusList": list(class_status),
                "nowTeacherIds": list(teacherids)
            }
        )

    # 查询班级信息
    def class_query_info(self, classid: int = None) -> dict:
        """
        查询指定班级信息
        :param classid: 班级id
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-pc-edu/classInfo/getClassInfoVo",
            params={
                "_t_": timestamp(),
                "classId": classid
            }
        )["data"]

    # 查询班级学生
    def class_query_student(self, classid: int, inout: int = 1) -> list:
        """
        查询班级学生
        :param inout: **[1]** 当前在班学员 **[2]** 历史学员
        :param classid: 班级ID
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-pc-edu/classStudent/queryClassStudentList",

            params={
                "_t_": timestamp(),
                "nameOrPhone": "",
                "classId": classid,
                "page": {"pageNum": 1, "pageSize": 100, "count": True},
                "inOut": inout
            }
        )["data"]

    # 取得收据信息
    def payments_query_receipt(self, orderinfo_id: int, payment_groupid: int) -> dict:
        """
        取得收据信息。
        :param orderinfo_id: 订单 ID
        :param payment_groupid: 支付 ID
        :return:
        """
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-pc-edu/public/receipt/findReceipt",
            params={
                "orderInfoId": orderinfo_id,
                "paymentGroupId": payment_groupid,
                "_t_": timestamp()
            }
        )["data"]

    # 查询指定订单组详情（APP接口）
    def order_group_detil(self, orderinfo_id):
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-edu/orderInfo/get",
            params={
                "orderInfoId": orderinfo_id,
                "_t_": timestamp()
            }
        )["data"]

    # 查询招生来源
    def comefroms_query(self):
        return self.request(
            method="get",
            url=f"https://{self.host}/api/cs-crm/customField/get",
            params={"_t_": timestamp(), "customFieldId": "26118419"}
        )["data"]["selectItemList"]
