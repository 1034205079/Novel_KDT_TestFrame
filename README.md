我用的python3.8

安装依赖库，国内卡就加个清华源 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package


        1. 读取excel：pip install openpyxl
        2. 操作mysql：pip install pymysql
        3. requests库：pip install requests
        4. selenium库：pip install selenium
        5. 报告服务器：pip install flask
        6. 报告邮件：pip install yagmail
        7. 加解密模块：pip install pycryptodome

 自行安装MySQL5.6，对应的表结构如下：

        库名儿：kdt_test

        已下为创建表结果的sql代码，可以放入到一个文本中保存为sql后缀格式，再通过navicat导入即可
        
        SET NAMES utf8mb4;
        SET FOREIGN_KEY_CHECKS = 0;
        
        -- ----------------------------
        -- Table structure for details
        -- ----------------------------
        DROP TABLE IF EXISTS `details`;
        CREATE TABLE `details`  (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `report_time` datetime(0) NULL DEFAULT NULL,
          `case_no` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `execute` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `case_module` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `case_function` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `case_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `result` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
          `errorinfo` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
          PRIMARY KEY (`id`) USING BTREE
        ) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;
        
        -- ----------------------------
        -- Table structure for result
        -- ----------------------------
        DROP TABLE IF EXISTS `result`;
        CREATE TABLE `result`  (
          `id` int(10) NOT NULL AUTO_INCREMENT,
          `report_time` datetime(0) NULL DEFAULT NULL,
          `case_total` int(10) NULL DEFAULT NULL,
          `case_pass` int(10) NULL DEFAULT NULL,
          `case_fail` int(10) NULL DEFAULT NULL,
          `case_skip` int(10) NULL DEFAULT NULL,
          PRIMARY KEY (`id`) USING BTREE
        ) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;
        
        SET FOREIGN_KEY_CHECKS = 1;

               
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

2. 写用例？不，先熟悉关键字库再写！在keyword目录下

BuildInLibrary：

        1. 包含了sleep：可以在自动化的时候用
        2. get_glob_paramter和set_glob_paramter：获取和设置全局参数，也封装了一些不同类型的时间戳，可以自己定义自己需要的时间戳。
        3. 替换参数：设置自定义参数后，使其生效返回对应的值

MyEncryptLibrary：

        1. 存放des加密和获取token的关键字库
        2. 可自行添加其他的加解密


MyPyKeyBoardLibrary：

        1. 封装鼠标键盘的库，用于模拟鼠标键盘操作
        2. 可以自行添加


MyRequestsLibrary：

        1. 发送请求的库
        2. requests方法：第一个位置参数为请求方式（POST,GET等），第二位置参数为url地址如\goods\list
        后面为不定长参数，用于接收，body或是url等参数
        3. assert开头的方法：为各类的断言方法
        4. get_value_from_response_re：从响应中提前一个值，并存储用于下一个请求里的参数。就是接口关联


MySeleniumLibrary：

        1. 封装web自动化的方法库，需要下载对应浏览器的dirver并放到python目录下
        2. open_browser：打开浏览器的方法，需要传入浏览器类型，如输入谷歌，火狐等，支持英文名
        3. maximize_browser_window：最大化窗口
        4. set_implicitly_wait： 设置隐式等待，需要传入timeout时间
        5. go_to： 打开你的地址
        6. my_find_element\my_find_elements：查找单个元素和多个元素的方法，传参例子xpath=//*[@xxx=xx],不只是xpath
        7. input_text：输入文本，传参和上面一样的，默认清空文本
        8. input_password：输入密码，传参和上面一样的
        9. click_element：点击元素，传参。。。
        10. element_should_be_visible：断言元素可见
        11. close_browser：管理浏览器
        12. assert_elements_len_should_be：断言元素长度
        13. get_element_text：获取元素文本

开始写用例~：

        1. 新建一个excel到case根目录，复制demo里的第一行列名到你的文件中
        2. 写一个简单request请求，加上断言如下图
        3. json或字典格式的参数，不要有空格，excel替换掉即可
        4. 具体怎么传参，还是要去看关键字里面的方法哈
![image](https://github.com/1034205079/Novel_KDT_TestFrame/assets/47485084/9b6c6009-aca5-4e5b-8bf8-e50f5b75b3bb)


启动测试：

        1. 这次只写了api测试的话，就运行runner_api即可
        2. 需要检查最底部，cases = ReadExcleCase('cases\API_test.xlsx').read_all_sheets() 是否执行正确的用例文件
        3. 若不需要发送邮件，就注释r.send_mail()
        4. 运行前，确保你的数据库可链接，并且账户授权了远程访问的权限
        5. 运行结束后，运行ReportServer.py开启测试报告服务
        6. 打开报告地址，查看报告
![image](https://github.com/1034205079/Novel_KDT_TestFrame/assets/47485084/2d6b01f1-2e7c-4f18-8921-358b519e2131)



















        





        
