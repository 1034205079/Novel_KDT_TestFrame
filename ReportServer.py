# html报告的服务
from flask import Flask
from Novel_KDT_TestFrame.tools.DBClass import DBClass
from Novel_KDT_TestFrame.config.config import Config

app = Flask("myreportservice")  # 实例化一个app

db = DBClass(**Config.db_info)  # 实例化一个数据库对象解包传入配置信息


@app.route("/result", methods=["GET"])  # 请求路径，请求方法
def result():
    with open(rf"{Config.project_path}\report\index.html", "r", encoding="utf8") as html:
        content = html.read()
        tr_td = ""  # <tr><td>1</td><td>2023-10-08 17:14:48</td><td>4</td><td>3</td><td>2</td><td>1</td></tr>
        # 数据库查询Summary数据
        db_summary_datas = db.query("select * from result order by id desc")
        for row in db_summary_datas:
            """加一个a标签替换 原来的time单元格"""
            tr_td += f'''<tr><td>{row.get("id")}</td><td><a href="/detail/{row.get("report_time")}">{row.get("report_time")}</a></td><td>{row.get("case_total")}</td><td>{row.get("case_pass")}</td><td>{row.get("case_fail")}</td><td>{row.get("case_skip")}</td></tr>'''
        # 替换html模板中的{summary_data}
        content = content.replace("{summary_data}", tr_td)
    return content  # 响应的body


# detail的页面
@app.route("/detail/<string:report_date>", methods=["get"])  # <string:report_date> 保存一个字符串变量 report_date
def detail(report_date):
    print("获取的url中的report_date 值为--->", report_date)
    with open(rf"{Config.project_path}\report\detail.html", "r", encoding="utf8") as html:
        content = html.read()
        tr_td = ""  # <tr><td>1</td><td>2023-10-08 17:51:31</td><td>test_login_api_01</td><td>Y</td><td>用户</td><td>登录</td><td>输入正确的账号登录成功</td><td>pass</td><td>无</td></tr>
        # 数据库查询detail数据
        db_detail_datas = db.query(f'select * from details where report_time="{report_date}"')
        for row in db_detail_datas:
            tr_td += f'''<tr><td>{row.get("id")}</td><td>{row.get("report_time")}</td><td>{row.get("case_no")}</td><td>{row.get("execute")}</td><td>{row.get("case_module")}</td><td>{row.get("case_function")}</td><td>{row.get("case_title")}</td><td>{row.get("result")}</td><td>{row.get("errorinfo")}</td></tr>'''
        # 替换模板中的{detail_data}
        content = content.replace('{detail_data}', tr_td)

    return content  # 响应


if __name__ == '__main__':
    print(f"http://{Config.windows_ip}:9999/result")
    app.run(host=f"{Config.windows_ip}", port=9999, debug=True, )
