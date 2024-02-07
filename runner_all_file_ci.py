import sys, traceback, time, html, os, glob

sys.path.append("D:\pythonProject")  # 设置路径，可配合jenkens使用
from Novel_KDT_TestFrame.config.config import Config
from Novel_KDT_TestFrame.tools.ReadExcleCase import ReadExcleCase
from Novel_KDT_TestFrame.tools.DBClass import DBClass
from Novel_KDT_TestFrame.tools.MyLogger import mylogger  # 直接导入实例化


class Runner(object):
    library_instance = {}  # 存储实例化的关键字对象 {“关键字”:关键字对象实例,....}

    def __init__(self):
        self.db = DBClass(**Config.db_info)

    @classmethod
    def get_library_instance(cls, library_name):
        if library_name not in cls.library_instance:  # 不存在则应该实例化
            # 1.动态导入模块
            module_name = library_name  # 模块名
            keyword_path = f"{Config.project_name}.keyword"  # 关键字路径
            keyword_path_module = f"{keyword_path}.{module_name}"  # 关键字和模块名拼接在一起
            __import__(keyword_path_module)  # 导入模块， 模块名是字符串，并且是完整的路径（从根目录开始导入）
            md = sys.modules[keyword_path_module]
            # 2.导入类
            # 我设计的关键字模块名和类 同名字
            keyword_cls = getattr(md, module_name)
            # 3.实例化
            instance = keyword_cls()  # 我的设计是构造方法不需要传入参数
            mylogger.info("新创建了一个关键字实例-->" + str(instance))
            # 4.保存一下
            cls.library_instance[library_name] = instance
        return cls.library_instance[library_name]

    def run_one_case(self, case=None):
        # case = {'用例编号': 'test_login_01',
        #         '是否执行': 'Y',
        #         '用例模块': '用户',
        #         '用例功能': '登录',
        #         '用例标题': '输入正确的账号登录成功',
        #         '测试步骤': [['打开浏览器', 'MySeleniumLibrary', 'open_browser', 'chrome'],
        #                      ['最大化浏览器', 'MySeleniumLibrary', 'maximize_browser_window'],
        #                      ['输入网址', 'MySeleniumLibrary', 'go_to', 'http://1.14.44.5:8080/'],
        #                      ['输入用户名', 'MySeleniumLibrary', 'input_text', 'id=username', 'admin'],
        #                      ['输入密码', 'MySeleniumLibrary', 'input_password', 'id=password1', 'admin123'],
        #                      ['输入验证码', 'MySeleniumLibrary', 'input_text', 'id=verifycode', '11xx'],
        #                      ['点击登录', 'MySeleniumLibrary', 'click_element',
        #                       'class name=form-control.btn-primary'],
        #                      ['断言', 'MySeleniumLibrary', 'element_should_be_visible', 'link text=注销', 10],
        #                      ['关闭浏览器', 'MySeleniumLibrary', 'close_browser']]}
        mylogger.info(
            f"开始执行用例-->{case.get('用例编号')}  -->{case.get('用例模块')}-->{case.get('用例功能')}-->{case.get('用例标题')}")
        if case.get("是否执行") not in ("Y", "y"):
            case["执行结果"] = "skip"
            case["执行信息"] = "无"
        else:
            for step in case.get("测试步骤"):
                mylogger.info("开始执行步骤-->" + step[0])
                try:
                    # 3.获取实例
                    instance = self.get_library_instance(step[1])
                    # 4.获取实例上的方法
                    method = getattr(instance, step[2])
                    # 5.运行实例方法
                    method(*step[3:])  # 传入必要的参数
                except:
                    mylogger.info("  步骤执行  失败")
                    case["执行结果"] = "fail"
                    case["执行信息"] = traceback.format_exc()  # 记录全面的错误信息
                    mylogger.info(case["执行信息"])
                    break  # 一个步骤失败，后面的步骤就不用执行了
                else:
                    mylogger.info("  步骤执行  通过")
            else:  # for .. break .. else
                case["执行结果"] = "pass"
                case["执行信息"] = "无"
        mylogger.info(f"结束执行用例-->{case.get('用例编号')} -->  {case['执行结果']}")
        mylogger.info("-" * 60)

    def run_all_case(self, case_list):
        self.case_list = case_list  # 绑定在实例上
        for case in self.case_list:
            self.run_one_case(case)

    def show_result(self):
        """展示运行结果"""
        case_total = 0  # 总数
        case_pass = 0  # 通过数
        case_fail = 0  # 失败数
        case_skip = 0  # 跳过数
        for case in self.case_list:
            case_total += 1  # 总数加1
            if case.get("执行结果") == "pass":
                case_pass += 1
            elif case.get("执行结果") == "fail":
                case_fail += 1
            elif case.get("执行结果") == "skip":
                case_skip += 1
        self.summary_message = f"所有用例执行完成：总数{case_total},通过数：{case_pass},失败数：{case_fail}，跳过数：{case_skip}。"
        mylogger.info(self.summary_message)
        self.report_time = time.strftime('%Y-%m-%d %H:%M:%S')  # 记录本次报告的时间
        # 1.插入汇总报告结果
        self.db.update("insert into result(report_time,case_total,case_pass,case_fail,case_skip) "
                       f"values('{self.report_time}',{case_total},{case_pass},{case_fail},{case_skip})")
        # 2.插入用例执行信息结果

        for case in self.case_list:
            # 遇到一个问题：用例的错误信息中有引号，打乱了sql语句，导致sql不能执行。
            # 解决：存入的sql信息最后需要在html中呈现，因此可以进行html转码，去掉引号。
            case_error_info = html.escape(case.get('执行信息'))
            case_error_info = case_error_info.replace("\n", "<br>").replace("\\", "\\\\")  # 优化页面html显示格式
            self.db.update(
                'insert into details(report_time,case_no,execute,case_module,case_function,case_title,result,errorinfo)'
                f'''values("{self.report_time}","{case.get('用例编号')}","{case.get('是否执行')}","{case.get('用例模块')}","{case.get('用例功能')}","{case.get('用例标题')}","{case.get('执行结果')}","{case_error_info}")''')

    def find_cases_by_dir(self):
        work_path = os.path.join(Config.project_path, "cases")
        cases_list = []
        files = glob.glob(f"{work_path}/[!~]*.xlsx", recursive=True)
        for f in files:
            cases_list.extend(ReadExcleCase(f).read_all_sheets())
        return cases_list


if __name__ == '__main__':
    r = Runner()
    cases = r.find_cases_by_dir()
    r.run_all_case(cases)
    r.show_result()
