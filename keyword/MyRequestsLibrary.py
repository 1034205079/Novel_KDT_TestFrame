import requests, json, re
from Novel_KDT_TestFrame.config.config import Config
from Novel_KDT_TestFrame.keyword.BuildInLibrary import BuildInLibrary


class MyRequestsLibrary(BuildInLibrary):
    def __init__(self):
        self.r = requests.session()

    def requests(self, method, url, *args):
        """发起请求"""
        datas = {}
        for arg in args:
            k, v = arg.split("=", maxsplit=1)
            v = self.replace_parameter(v)  # 替换v中的{{变量}}
            datas[k] = eval(v)  # 转为字典
        self.response = self.r.request(method, Config.base_url + url, **datas)

    def assert_status_code(self, status_code):
        """断言响应状态码"""
        assert self.response.status_code == int(status_code)

    def assert_response_headers(self, key, value):
        """断言相应头"""
        assert value in self.response.headers.get(key)

    def assert_response_value_equal(self, key, value):
        """断言相应值相等"""
        assert self.response.json().get(key) == value

    def assert_response_body_in(self, body):
        """断言相应body包含"""
        assert body in self.response.text

    def assert_response_json_equal(self, expect_json):
        """断言响应json相等"""
        response_json = self.response.json()  # 获取响应的json，并转为python数据格式
        expect_json = json.loads(expect_json)  # 把json转为python数据格式
        assert response_json == expect_json

    def assert_response_json_len(self, length):
        """断言响应json的长度"""
        assert len(self.response.json()) == int(length)

    def get_value_from_response_re(self, save_param, pattern):
        """通过正则保存值"""
        key = re.fullmatch("\{\{(\w+)}}", save_param).group(1)  # 获取参数名
        value = re.search(pattern, self.response.text).group(1)  # 正则匹配
        self.set_global_parameter(key, value)  # 保存参数到全局变量中
