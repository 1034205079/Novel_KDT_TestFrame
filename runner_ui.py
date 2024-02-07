import sys, traceback
from Novel_KDT_TestFrame.tools.ReadExcleCase import ReadExcleCase
from Novel_KDT_TestFrame.config.config import Config


class Runner:
    library_instance = {}  # 存储实例化的关键字对象 {“关键字”:关键字对象实例,....}

    @classmethod
    def get_library_instance(cls, library_name):  # keyword
        if library_name not in cls.library_instance:
            module_name = library_name  # 获取 MySeleniumLibrary
            lib_path = f"{Config.project_name}.{module_name}"  # 写的库的路径
            __import__(lib_path)  # 导入模块， 模块名是字符串，并且是完整的路径（从根目录开始导入）
            md = sys.modules[lib_path]  # 获取库路径
            """动态导入类"""
            keyword_cls = getattr(md, module_name)  # 可以获取到md里面的类
            instance = keyword_cls()  # 实例化类
            """保存"""
            cls.library_instance[library_name] = instance
        return cls.library_instance[library_name]

    def run_1_case(self, case):
        print(
            f"开始执行用例-->{case.get('用例编号')}  -->{case.get('用例模块')}-->{case.get('用例功能')}-->{case.get('用例标题')}")
        if case.get("是否执行") not in ("y", "Y", "yes", "Yes"):
            print("已跳过执行用例")
        else:
            for step in case.get("测试步骤"):
                print("开始执行步骤-->", step[0])
                try:
                    instance = self.get_library_instance(step[1])  # 获取 MySeleniumLibrary
                    method = getattr(instance, step[2])  # 4.获取实例上的方法,例如open_browser
                    method(*step[3:])  # 5.运行实例方法
                except:
                    print("  步骤执行  失败")
                    execute_info = traceback.format_exc()  # 执行信息
                    print(execute_info)
                    break  # 一个步骤失败，后面的步骤就不用执行了
                else:
                    print("  步骤执行  通过")
            else:
                case["执行结果"] = "pass"
        print(f"结束执行用例-->{case.get('用例编号')} -->  {case['执行结果']}")
        print("-" * 60)

    def run_all_case(self, case_list):
        for case in case_list:
            self.run_1_case(case)


if __name__ == '__main__':
    file = "cases/UI.xlsx"
    # cases = ReadExcleCase(file).read_by_sheet("test_customer")
    cases = ReadExcleCase(file).read_all_sheets()
    r = Runner()
    r.run_all_case(cases)

