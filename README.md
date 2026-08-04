这是一个pytest+allure+request实现的接口自动化测试项目，测试所用的接口来自于github api

这个项目具备以下功能：

- fixture实现测试环境准备（所有请求头加token）
- 测试数据解藕/json数据驱动（测试数据包含接口传参用例和接口响应断言）
- 接口请求参数化
- 接口依赖
- allure生成测试报告
- 日志管理
- 测试用例顺序管理

# 功能0-fixture实现测试环境准备

- 在测试用例目录下新建一个conftest.py, 在这个文件里定义一个装饰器fixture,将属性autouse=True, scope=”session”
- 该fixture实现了在发起http请求时，在所有请求头加上token
- 需要RequestUtil工具类配合，使用单例模式，并且类属性session也要实现单例模式

# 功能1-测试数据解藕

目的：为了保证接口信息更改，测试用例数据修改，接口响应断言方式改变，不会影响代码，**实现代码和用例的解藕**

实现方式：data+util+api

1. 接口测试用例数据层data：
    1. 所有接口通用的信息（如base_url, headers)存储在config.yaml中
    2. 单个接口的url和method(get post)存放在data/{module_name}/xx_xx_api.json中
    3. 每个接口的测试用例数据（也就是用例名称、请求参数、预期响应、用例类型）用json 数组的形式存放在data/{module_name}/xx_xx_cases.json中
2. 工具层：
    1. 负责处理存储通用接口信息的yaml文件和存储接口测试用例数据的json文件
        1. yaml_util.py中的read_config_yaml函数实现了以下功能：
            1. 可读取yaml嵌套字典中的值
            2. 依赖PyYAML中的yaml.load(f,yaml.SafeLoader)函数将yaml文件转换为python对象
        2. 做了以下两点优化：
            1. 将函数形参转换为可变长度参数
            2. 做了预防空指针处理
        3. json_util.py中的read_json函数使用json.load(fp)函数将json文件中的接口信息转换成python字典
        

## 功能2到底是如何实现测试数据的参数化？

### json文件驱动

### 用例标记：每个用例json对象有一个case_type字段，case_type有固定值all,normal,exception，config.yaml里定义case_type选定的值

read_json函数传入一个形参，即config.yaml文件中case_type的值，用列表生成式的if条件进行筛选，这样就可以进行用例的筛选。

如果你只想执行正常流程，那么config.yaml里写normal,那么就只会执行json文件里被标记为case_type:normal的用例

### 使用pytest的parametrize装饰器

@pytest.mark.parametrize(参数名，参数列表）参数列表传入read_json读取到的json对象列表，

即可实现单个测试函数用多组测试数据执行多次，

也就是测试数据参数化,实现了json数据驱动+pytest parametrize装饰器结合

### 接口请求参数化：

测试数据json文件中请求参数可以传“get_fun_xx（xx..)”或者”select …“sql语句，

遍历这个json对象时，如果识别到有json值以get_fun_或者select开头，或是请求路径/请求体中包含`${variable}`这个表达式

get_fun_会将这个字符串用eval转换成python表达式，去调用GetFunUtil类的同名方法

以select开头，方法会将这个sql命令传给ShellUtil里的处理sql语句的函数，获取sql返回值

求路径/请求体中包含`${variable}，` 去变量池（一个session级别的返回字典的fixture)取以variable作为key的值

最后用处理过的值替换json文件里的值

## 如何实现接口响应断言机制？

### 断言的分类：

- 响应时间断言
    - 这个基本是所有接口通用的，所以我选择写在config.yaml
- 状态码断言：
    - 每个接口请求成功的响应码可能是不同的，有的是200，有的是201，如果异常测试用例，状态码有可能是403 404等，
    - 所以我写在data/{module_name}/xx_xx_cases.json测试用例json文件expected字段中）
- body断言
    - 字段存在性断言
    - 字段固定值断言
    - 更复杂的还未接触到，对于body我选择json schema这种语法格式去描述json数据

### 断言的实现

封装了一个AssertUtil类，

- 实现了统一的异常处理
    
    每一类断言对应一个函数，这些函数内部不做异常处理，放到最后总的函数去做异常处理，减少冗余代码
    
    如果断言抛出异常了，那么断言一定是失败的
    
- 断言字段可灵活配置
    - 不需要进行该类断言时，直接不要在yaml或者json文件里配置即可
    - 因为每一类断言函数都进行了空值处理，is None成立时在日志里打印提醒一下，之后直接return，跳过之后的代码
- 断言名称可以在allure测试报告中展示
    - 用了with allure.step(f””)

# 功能 3 - 接口依赖

1. 变量池：定义一个session级别的 返回字典的 fixture
2. jsonpath提取响应体字段: 将Jsonpath写到测试用例json文件中，用jsonpath取响应体字段值，存到变量池
3. 识别接口依赖变量：正则表达式匹配`${variable}`表达式
4. 用匹配结果作为key去变量池取值替换

# 功能4- allure实现测试报告

1. 安装allure，在requirements.txt里加上allure-pytest依赖
2. 用例中添加装饰器/注解@allure.epic feature story step/with allure.step() allure.dynamic.title()，使得测试报告里有项目名称 模块名称 测试用例名称 步骤名称 测试用例名称
3. 执行测试用例时生成json数据，在pytest.main里添加—alluredir xxx —clean-alluredir 
4. 将生成的json数据转换成html格式的测试报告 os.system(allure generate json文件目录 -o 测试报告目录 —clean)

测试报告展现测试用例成功/失败结果，失败原因

# 功能5-日志管理

- 使用loguru.add(sink参数实现了三重日志输出：控制台、日志文件、allure测试报告
- 使用magic method new方法实现了LogUtil的单例模式
- 分级输出，不同level的日志输出到不同的日志文件中

# 功能6 - 测试用例顺序管理

当前主流替代是**活跃维护**的 `pytest-order` 插件，用 `@pytest.mark.order()`

有一些新特性相对顺序和first last等新特性，可以了解一下
