from Novel_KDT_TestFrame.keyword.BuildInLibrary import BuildInLibrary
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import json, base64, hashlib, time

"""这是加密请求参数的类，然后生成token"""


class MyEncryptLibrary(BuildInLibrary):

    def des_encrypt(self, raw_str, key):  # des加密请求参数
        plaintext_string = json.dumps(eval(raw_str))  # 将未加密的数据转换为json格式,excel读出来的是字符串需要eval格式化成字典
        cipher = DES.new(key.encode(), DES.MODE_ECB)  # 创建一个DES实例
        padded_message = pad(plaintext_string.encode(), DES.block_size)  # 对字符串进行填充
        encrypted_message = cipher.encrypt(padded_message)  # 加密填充后的字符串
        self.en_str = base64.b64encode(encrypted_message).decode()  # 将加密后的字符串转换为base64格式
        self.set_global_parameter("en_str", self.en_str)  # 保存加密后的字符串到全局变量中
        return self.en_str  # 返回加密后的字符串

    def get_token(self):  # 获取token
        md5_hash_1 = hashlib.md5(self.en_str.encode()).hexdigest().lower()  # 对字符串进行第一次MD5哈希并转换为小
        raw_token_str = "ludashi_" + md5_hash_1 + "_mikannovel_android"  # 构建待加密字符串
        self.my_token = hashlib.md5(raw_token_str.encode()).hexdigest().lower()  # 对构建好的字符串进行第二次MD5哈希并转换为小写
        self.set_global_parameter("my_token", self.my_token)  # 保存生成的token到全局变量中
        return self.my_token  # 返回生成的token
