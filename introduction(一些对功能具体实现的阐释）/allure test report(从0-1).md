ref：https://allurereport.org/docs/v2/

https://www.cnblogs.com/poloyy/p/12712616.html

https://www.cnblogs.com/poloyy/p/12725509.html

# 1. 安装(mac)

### **从压缩包安装**

1. 请确保已安装 Java 8 或更高版本，并且已在环境变量中指定其目录`JAVA_HOME`。
2. 前往**GitHub 上的最新 Allure Report 版本**并下载`allure-*.zip`其`allure-*.tgz`存档。
3. 将压缩包解压到您选择的安装目录。例如：
    
    ```
    tar xf /home/user/Downloads/allure-2.29.0.tgz -C /home/user/tools
    ```
    
4. 打开登录时命令行 shell 加载的脚本（它可能位于`~/.profile`、`~/.bash_profile`、`~/.zprofile`等位置），并在其末尾添加以下行。
    
    （请将此处替换为安装目录中子目录文件`/home/user/tools/allure-2.29.0/bin`的路径。）`bin`
    
    ```
    export PATH=$PATH:/home/user/tools/allure-2.29.0/bin
    ```
    
5. 如果您之前已将其他版本的 Allure Report 的路径添加到`PATH`，请务必将其删除。
6. 关闭并重新打开终端窗口。
7. 运行此命令以查看是否报告最新版本：
    
    ```
    allure --version
    ```
    

## 安装pytest-allure依赖

```python
(venv) chensiyue@magicBook pytest_learning % pip install allure-pytest

```

验证：

```python
(venv) chensiyue@magicBook pytest_learning % pytest --help | grep allure

```

# 2.生成测试报告

```python
 pytest --alluredir=./allure_report --clean-alluredir
```

测试用例执行结果存放在./allure_reports下,每一条测试用例对应一个JSON文件，json文件中存放测试用例的名字 开始时间 结束时间 执行结果

--alluredir用于指定存储测试结果的路径

--clean-alluredir: 在运行测试前，先把旧的alluredir里面的结果删掉清空

**`*note: 如果alluredir不存在，会自动创建此目录*`**

# 3.查看测试结果

## 方式1:

Json生成html网页，存放在某个临时目录下，直接通过默认浏览器打开

```python
 allure serve ./allure_reports 

```

## 方式2:

先对json结果文件生成html

```python
allure generate ./result/ -o ./report/ --clean
```

### ./result:  --alluredir=生成的Json文件

### -o ./report:

👉 output 输出目录

意思是：

> 把“漂亮的HTML报告”生成到 `./report/`
> 

生成后里面会有：

- index.html（入口）
- css/js
- 各种静态资源

👉 本质：**给人看的网页报告**

### —clean: 每次生成报告前，先删除./report文件夹

再打开html,命令行或者注解打开index.html都可以

```python
 allure open -h 127.0.0.1  ./allure_reports/

```

# 4测试报告

!image.png

如果有pytest.fixture ，是会体现在测试报告的setup teardown中的

如果有pytest.mark.parametrize,也是会体现在测试报告的parameters中的

测试报告按package-module-class-function的分类展示测试用例

# 5. environment.properties

在存放`json文件的目录(即alluredir)`下 ，新建environment.properties

```python
systemVersion=macOS Monterey
pythonVersion=3.11
allureVersion=2.44.0
projectName=pytest_learning
```

在测试报告的environment就会出现自定义的环境配置

!image.png

# 6.标记装饰器epic feature story step

- @allure.epic(””)史诗，比如SC50
- @allure.feature(””)模块，功能点，testsuite比如地图管理
- @allure.story(””)测试用例名称 ,子功能名称，testcase

从上到下有层级

epic和feature一般写在class上面，story写在具体的测试方法上

作用：将测试报告里的测试用例结果分类显示

- @allure.step(””)一般放在不是以test_开头的普通方法上，当方法之间嵌套会比较有用，否则的话只会显示一个步骤； 只有一个参数，字符串，就是title，你传什么，在allure上就显示什么；，支持位置参数 {0},{1};关键字参数{arg1},{arg2}, 在allure测试报告里也会显示；

```python
import allure
import pytest

@allure.epic("pytest学习")
@allure.feature("allure模块")
class TestA:
    def test_b(self):
        print("/n"+"*"*12)

    @pytest.mark.parametrize("arg",[1,2])
    def test_a(self,login,arg):
        assert arg==1

    @allure.step("第一步")
    def step_1(self):
        pass

    @allure.step("第二步,{arg1},{arg2}")
    def step_2(self,arg1,arg2):
        pass

    @allure.story("测试step装饰器")
    def test_c(self):
        self.step_1()
        self.step_2(3,4)

```

!image.png

```python
Day6::test_allure.py
import os

import allure
import pytest

@allure.step("第一步")
def step1():
    pass

@allure.step("第二步----{0},{1}")
def step2(arg1, arg2):
    pass

@allure.step("第三步,{arg1}")
def step3(arg1):
    pass
@pytest.mark.smoke
@allure.epic("SC50")
@allure.feature("地图管理模块")
class TestMap:
    @allure.step("确认是否存在同名地图")
    def check_same_map(self,map_name):
        pass
    @allure.story("预制地图")
    def test_pre_map(self):
        step1()
        step2(2,3)
        step3(arg1=1)

    @allure.story("创建地图")
    @pytest.mark.parametrize("map_name",['5F','5F_1'])
    def test_create_map(self,map_name):
        self.check_same_map(map_name)

@pytest.mark.smoke
@allure.epic("SC50")
@allure.feature("路径管理模块")
class TestPath:
    @allure.story("新建路径")
    def test_create_path(self):
        pass

main.py
import os

import pytest

if __name__ == "__main__":
    alluredir = "./temp"
    report_path = "./allure_reports"
    pytest.main(["--alluredir", alluredir, "--clean-alluredir"])
    os.system(f"allure generate {alluredir} -o {report_path} --clean")
    os.system(f"allure open {report_path} ")

```

!image.png

# 7 with allure.step(””): assert

用来在测试方法中添加测试步骤

## 为什么要用with

```python
def check_result():
        with allure.step("检查测试结果"):
            assert True
```

相当于

```python
def check_result():
        step=allure.step("检查测试结果")
        step.__enter__()
        assert True
        step.__exit__(None,None,None)
```

效果和@allure.step()一致

!image.png

# 8 测试用例执行过程中动态指定测试标题

ref:https://www.cnblogs.com/poloyy/p/13894043.html

```python
	 @allure.story("create issue")
    @pytest.mark.parametrize('case',cases)
    def test_create_issue(self,case):
        """取测试用例名称，allure动态指定"""
        case = convert_json(case, self.cases_path)
        case_title = case.get("title")
        ***allure.dynamic.title(case_title)***
        r = send_request(method=self.method, url=self.url, headers=self.headers, playload=case["data"])
        AssertUtil.check_res(r, case, case_title)

```