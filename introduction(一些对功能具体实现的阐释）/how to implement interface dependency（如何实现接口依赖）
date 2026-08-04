# 什么是接口依赖？

B的请求参数依赖A接口的响应字段

举个🌰：

github api: create an issue响应体中返回issue number; get an issue的请求参数需要issue number

# 如何实现接口依赖？

## 第一步：jsonpath 提取接口响应的字段，存储到类范围内的fixture

在用例中添加extract字段，如下，需要提取接口响应体中的number字段，并且用issue_number作key存储到变量池中

```bash
    "extract": {
      "issue_number": "$.number"
    }
```

!image.png

变量池是conftest.py中定义的session级别的fixture,这个fixture返回一个空字典，用这个是因为很方便函数传参

注意因为是会话级别的，且字典里的变量名具有唯一性，所以给这个空字典塞k-v的时候注意变量取名的唯一性

conftest.py

```python
@pytest.fixture(scope="session")
def api_deps():
    """存储接口依赖字段的全局字典（如token、user_id等）"""
    return {}
```

在测试方法中发起http请求获得响应后，用extract中的jsonpath对接口响应进行字段提取

!image.png

extract_json_value()函数干了什么？

根据json文件中的extract字段，用jsonpath提取响应体中的 值 存储进变量池

如下：

```python
def extract_json_value(data, case, api_deps):
    """
    从响应体中提取json_path对应的值
    :param data: 响应的json体对象
    :param case: 从json文件中提取类似于"$.number"的jsonpath,
    :return:
    """
    # 首先从json中提取extract字段，如果为空，则不继续进行下面的代码
    extract = case.get("extract")
    if extract is None:
        return
    for k, v in extract.items():
        # 从响应体中提取json_path对应的值,⚠️，这是一个列表
        parse_results = jsonpath.jsonpath(data, v)
        if parse_results:
            # 如果列表不为空，取第一个值
            api_deps[k] = parse_results[0]

```

## 第二步:URL path参数替换 和请求参数替换

识别变量：我们在第一步取了响应字段存到变量池里，那么下一步我们要如何告诉程序 **这个变量是需要去变量池取值替换的**？

我采取的方式是在需要取变量值的地方，定义一个表达式：`${issue_number}`

这个表达式可以放到一个字符串里面，如下

举个🌰：

```python
{
  "path": "/repos/miri90/wenda/issues/**${issue_number}**",
  "method": "patch"
}
```

也可以直接整个值就是这个表达式，如下

```json
{
	"issue_number":${issue_number}	
}
```

那么我们程序要如何去**识别**这样一个表达式呢？

用正则表达式去匹配`${issue_number}，`正则如下：

```python
# 定义正则匹配规则：专门匹配 ${英文 / 数字}这种格式
pattern = r"\$\{(\w+)\}"
```

python如何进行正则表达式匹配替换

之后调用re(python专门用于正则匹配的依赖）的api去正则匹配取key,拿到key去变量池里取key对应 的value,之后用value去替换json请求体里的表达式`${issue_number}`

具体函数如下：

```python
def replace_variables(text, api_deps) -> str:
    """
    纯变量 ${issue_number} → 返回数字 8（GitHub 接口不报错）
    带文字的变量 /issues/${num} → 返回字符串（URL / 请求头正常用）
    1 第一种匹配类型 匹配：整个字符串就是变量，如 ${number},返回8，而不是"8"
    2 第二种匹配类型 匹配：字符串中包含变量（如 /issues/${num}），全局替换,返回"/issues/8"
        把path字符串里的 ${变量名} 替换成真实的值
        比如：/issues/${issue_number} → /issues/123
        替换字符串中的${变量}
        支持:
        /issues/${issue_number}
        /users/${user_id}/issues/${issue_number}
        无变量:
        /issues/list
    :param text:
    :param api_deps:变量池
    :return:处理过后的text
    """
    ''' 1. 判断：如果传入的text不是字符串（比如是数字 / None/bool）'''
    # 直接返回原值，不做任何处理（防止报错）
    if not isinstance(text, str):
        return text

    # 定义正则匹配规则：专门匹配 ${英文 / 数字}这种格式
    pattern = r"\$\{(\w+)\}"

    """2. 第一种匹配：整个值就是纯变量 ${变量名},需要按照原有类型返回
    （因为是一般是放在请求参数里的，如果参数类型不对，是无法成功调通接口的）"""
    # 与 re.match() 不同，re.fullmatch() 要求整个字符串完全匹配正则表达式，而不是只从开头匹配。
    # 返回值： 如果整个字符串匹配，返回 match 对象；否则返回 None。
    match=re.fullmatch(pattern=pattern, string=text)
    if match is not None:
        key=match.group(1)
        # 判断：如果变量名不在api_deps字典里，直接报错
        if key not in api_deps:
            logger.debug(f"变量池不存在变量:{key}")
            raise ValueError(f"变量池不存在变量:{key}")
        # 从变量池里取值,⚠️核心：返回原始值，不转字符串！
        value = api_deps.get(key)
        return value

    '''3.第二种匹配：字符串中包含变量（如 / issues /${num}），全局替换'''
    def replace(match):
        key = match.group(1)
        # 判断：如果变量名不在api_deps字典里，直接报错
        if key not in api_deps:
            logger.debug(f"变量池不存在变量:{key}")
            raise ValueError(f"变量池不存在变量:{key}")
        # 从变量池里取值
        value = api_deps.get(key)
        # 这个函数必须返回字符串
        return str(value)

    # 用re.substitute函数进行正则匹配，并且为每一个匹配到的字符串调用replace函数，进行替换
    text = re.sub(pattern=pattern, repl=replace, string=text)
    return text
```

```python
def convert_json(json_obj, case_path,api_deps=None):
...(这里略去处理get_fun_xx(*args)和select开头的逻辑，只保留了如何处理${variable}的逻辑）
                        elif re.search(r"\$\{(\w+)\}",v) is not None:
                            extract_v=replace_variables(v,api_deps)
                            logger.debug(f"接口依赖解析结果是{extract_v}")
                            ReplaceJsonKey().replace_json_key(data,key,extract_v,i)
```

之后，在测试函数里调用这两个函数处理URL和请求参数

!image.png

# 既然涉及到接口b依赖接口a,那也就意味着接口a的执行顺序一定要早于接口b，否则如何提取接口a的响应值呢？

pytest框架的默认测试用例执行顺序：

- 不同package按照字典序执行
- 不同文件名按照字典序
- 同一个模块中按照模块中测试用例从上到下执行（不按照字典序）

当我们定义一个session级别的fixture，返回空字典作为变量池时，为了保证接口a早于接口b向变量池塞入k-v

需要引入第三方依赖    控制pytest测试用例执行顺序

当前主流替代是**活跃维护**的 `pytest-order` 插件，改用 `@pytest.mark.order()`

- 绝对排序：不要再用@pytest.mark.run(order=1)了，现在已经改成@ptest.mark.order(1)了
- 绝对排序对跨package 模块都是有效的
- 增加了`@pytest.mark.order(”first”). @pytest.mark.order(”last”)`新特性、
- 相对排序：`@pytest.mark.order(before=”测试函数名”) @pytest.mark.order(after=”测试函数名“）` 但这个只能保证测试函数b在测试函数a后执行，并不一定**严格保证测试函数b紧跟**在测试函数a之后运行
- 注解/装饰器的作用范围：类上/方法上；注解在类上就代表整个类的测试方法的执行顺序，类内的测试方法按照从上到下的顺序执行
