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
先修改配置文件config，
![image](https://github.com/1034205079/Novel_KDT_TestFrame/assets/47485084/de1777d2-d1fc-49b2-8266-e07d60b07640)
