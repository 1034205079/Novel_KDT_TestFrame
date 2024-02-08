我用的python3.8

安装依赖库，国内卡就加个清华源 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package


        1. 读取excel：pip install openpyxl
        2. 操作mysql：pip install pymysql
        3. requests库：pip install requests
        4. selenium库：pip install selenium
        5. 报告服务器：pip install flask
        6. 报告邮件：pip install yagmail
        7. 加解密模块：pip install pycryptodome
        

组件介绍：

        cases：存储测试用例的xlsx格式文件，包含demo。填写方式可参考demo
        config：框架配置文件（请求地址，数据库配置，邮箱配置等）
        keyword：封装好的关键字库
        log：存放日志文件
        report：报告模板，runner中替换元素
        tools：包含mysql数据库，excle读取，日志工具
        reportServer.py：测试报告服务，需要启动才能看报告
        runner：三种启动器，单独启动api测试，web自动化测试，全部一起测试（这个支持cmd启动）

如何使用？

1. 先修改配置文件config，
![image](https://github.com/1034205079/Novel_KDT_TestFrame/assets/47485084/de1777d2-d1fc-49b2-8266-e07d60b07640)

2.写用例？不，先熟悉关键字库再写！在keyword目录下

BuildInLibrary：

        1. 包含了sleep：可以在自动化的时候用
        2. get_glob_paramter和set_glob_paramter：获取和设置全局参数，也封装了一些不同类型的时间戳，可以自己定义自己需要的时间戳。
        3. 替换参数：设置自定义参数后，使其生效返回对应的值

MyEncryptLibrary：

        
