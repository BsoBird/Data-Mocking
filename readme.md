# Data-Mocking

## 简介

##### 1、Data-Mocking是什么？

  他是一个模拟数据生成器。我们在测试过程中，产生完整、全面的真实数据可能比较困难。
  我们可以根据需求，创建对应的模版和词典，利用数据模拟生成器生成我们需要的模拟数据。

##### 2、Data-Mocking能做什么？

  他能够根据构建的模版和词典，生成我们需要的数据。kafka需要的数据，hive中文件存储数据，接口中JSON数据等等，只要有数据格式，都可以设置成需要的模板。

##### Data-Mocking三个应用场景：

*   测试场景

    测试过程中，我们需要验证数据后端的功能或性能，此时，需要降低与数据产生端的耦合，那么需要一个稳定优秀的数据生成器，来持续的不间断的产生正确的数据，和特殊情况下的异常数据。

*   持续集成场景

    在整个持续集成场景中，一个或多个模块组成一个平台，需要有源源不断的数据进入持续集成环境，用以自动化地完成测试和迭代工作，使用Data-Mocking则可以通过数据样本的指定和简单的编码，非常简单地完成这个需求。

*   生产场景

    在一个项目完成测试和迭代，发布到生产环境之后，通常也需要进行持续的功能或可用性监测，那么则需要有各种正常或异常数据按照某种规则和定义，持续稳定地生产并送回平台，此时将持续集成场景中的case，只需通过简单配置，则可以进行生产的验证，以满足这个需求。

##### 3、架构

  数据生成器包括：模版变量提取，模版变量执行，模版变量替换三部分组成.

##### 4、术语：

*   函数变量:模版和词典中以`$FUNC{`开头,以`}`结尾的字符串是一个函数变量.形如：`$FUNC{intRand()}`. 其中,intRand()为内置函数. 支持函数嵌套.  
*   预编译函数变量:模版和词典中以`$FUNC_PRE{`开头,以`}`结尾的字符串是一个预编译函数变量.形如：`$FUNC_PRE{intRand()}`. 其中,intRand()为内置函数. 支持函数嵌套.预编译函数只在子模板执行的情况下才会生效,一般场景下他就是一个字符串。
*   模板变量：模版中以`$REF{`开头，以`}`结尾的字符串是一个词典变量。形如：`$REF{name}`,其中，name为词典中的一个词典名。允许模板变量相互引用。
 example:`$FUNC{dateStringWithRange($FUNC{long(123456789)},$FUNC{timestamp()},$REF{test_name})}`

##### 5、内置函数

*   可调用任意python基本函数,支持pyhton风格的函数传参.
Example:`$FUNC{name(a=1,b=2)}`

*   eval(str)
可执行任意python语句的表达式,若无法执行,则返回原值.
Example:`eval(1+2)`

*   concat(*args)
将传入的参数列表作为字符串拼接.

*   concat_ws(tag, *args)
将传入的参数列表按照指定的分隔符拼接.

*   Faker 模块中的任意mock数据的方法(目前faker的locate在这里被设置为了`zh-ch`,暂不支持变更locate).
详见`https://pypi.org/project/Faker/`
中文相关文档`https://zhuanlan.zhihu.com/p/87203290`

*   name(arg=None)若传入值,则返回传入值.否则随机生成name.

*   company(arg=None)
获取公司名称,若传入参数,则返回传入值,否则将随机生成.

*   age(arg=None)
获取随机的年龄,若传入参数,则返回传入值,否则将随机生成15~60内的数字.

*   Id(arg=None)
获取随机的ID,若传入参数,则返回传入值,否则将随机生成111111111111111111~911111111111111111内的数字.

*   timeNow(arg=None)
若传入参数,则返回传入值,否则将生成当前时间的时分秒.

*   dateNow(arg=None)
若传入参数,则返回传入值,否则将生成当前时间的年月日.

*   dateTimeNow(arg=None)
若传入参数,则返回传入值,否则将生成当前时间的年月日时分秒.  

*   quote_escaped(str_val)
将文字中的没有被转义的单引号与双引号进行转义.  

*   quote_replacement(str_val)
将字符串中的 $ 与 \ 进行转义.  

*   mock_default(mock_template,exec_times,result_concat_separator) 
我们支持在模板中利用另一个模板来生成数据,这种场景通常用于生成有嵌套结构,且内外层数据之间有关联关系。参数描述如下:  
    * `mock_template` : 传入的json模板,模板内容参照`章节6`  
    * `exec_times` : 模板执行次数,若传入-1且模板内`numb`属性大于0,则使用`numb`
    * `result_concat_separator` : 执行结果拼接的间隔符。因为生成的结果一定是字符串,所以只提供拼接功能。

*   mock_all_single(mock_template,exec_times,result_concat_separator)  
与`mock_default`方法接近,但是它与上面的区别是每次执行模板都是独立执行,保证不会生成相同数据

##### 6、基本使用指南

请使用post请求:  
- `http://host:port/help`  查看说明文档  
- `http://host:port/mockData`  产生N条不相同的数据
- `http://host:port/mockData/allsame`  产生N条完全相同的数据

下面是一个DEMO演示.  

body：

    {
        "content":"INSERT INTO table_name (name,age,dateTime) VALUES ('$FUNC{name($REF{p1})}', $FUNC{age()},'$FUNC{dateTimeNow()}')",
        "numb": 5,
        "function_dic":"{\"p1\":\"$FUNC{name()}}\""
    }
    

response:

    {
        "result": [
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 23,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 20,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 39,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27,'2020-07-31 00:35:55')"
        ],
        "num": 5,
        "dateTime":"2020-07-31 00:35:55"
    }

请求参数描述如下:  

*   `content` 待替换的模板
*   `numb` 一次生成多少条数据,一次生成不能超过1W条
*   `function_dic` 模板方法列表,可缺省。模板方法可以保证在一次mock数据的过程中,同样的模板生成的值始终相同.
 该参数可缺省,若缺省该参数,则不执行模板替换.若传入了该参数,但是传入的字典中没有`content`中出现的待替换的模板,则异常.支持模板方法之间相互引用.  
*   `circular_reference_parse_max_times` 循环引用最大解析次数,默认为1,可缺省。由于在`function_dic`中,我们允许模板方法之间相互引用,那么就存在N个模板相互引用形成循环引用的问题。
由于无限解析会出现死循环,这里我们做出限制,对于模板引用的解析只能执行N次,N次过后不再执行解析,会将形如`$REF{XXX}`的串直接返回。由于每解析一次,会将原串替换,最终并不能保证返回使用者处时传入的`$REF{XXX}`串。
 ##### 7、高阶使用指南
 * 特殊分隔符。我们有时需要使用特殊分隔符来拼接字符串产生结果,例如造hive的数据文件。由于python json包限制的原因,特殊字符需要传入对应的unicode码。例如`\x01`需要写`\u0001`
 * 使用逗号拼接。由于在函数解析的过程中,逗号往往是参数列表分隔的标识,而很多时候我们希望使用逗号拼接内容,这里我们处理成传入`\,` 来标识,涉及到的函数有`concat_ws`,`mock_default`,`mock_all_single`(详见example)。
 * 空白符的使用。由于在内部实现中,所有的方法的入参全部被trim了一次,因此,如果想实现类似给一个字符串拼接一个空白字符的功能,类似`concat('   ','a')`,是不能直接使用Function实现的。
 但是可以稍作变通,我们可以采取形如这样的方式实现`$FUNC{t1()}       $FUNC{t2()}`,在模板中留空白,这样就可以变相实现功能
 * 模板方法列表。对于过于复杂的模板片段,可以将它写入模板方法列表,在主模板中引用该片段即可,但这样做之后,该批次生成的数据,被引用的模板方法会生成完全相同的数据,若想生成不同的数据,需要调用多次。  
 * 子模板使用指南。我们支持使用`mock_default`和`mock_all_single` 方法通过子模板来生成数据,并将结果在主模板中使用。
 对于子模板,由于其可能较为复杂,我们最好将它也写入模板方法列表中。子模板的使用需要注意如下几点:
     * 由于整个模板引擎执行的过程中,是按照 `执行模板方法列表` -> `将执行模板方法列表执行结果替换主模板`  -> `执行模板中出现的方法(自顶向下LL)`  -> `将执行方法的结果替换模板`
     这样的顺序执行的。如果子模板中存在方法,那么会被优先执行,最终导致子模板执行的结果可能是完全一致的。若需要避免这种情况,子模板中的函数定义应使用`$FUNC_PRE{`.
     `底层方案`:`$FUNC_PRE{`不会触发方法执行,所有可以保证形如`$FUNC_PRE{xxx}`的串可以原样传入方法,在`mock_default`和`mock_all_single`方法中,会先将`$FUNC_PRE{`替换为`$FUNC`,
     这样再执行子模板就又可以触发方法执行。  
     * 子模板中若存在方法引用,会使用父模板中的模板方法列表进行替换,不会使用自己的,以此递归向下(如果你的子模板还套了子模板)


`Example`(生成嵌套结构的,内外有关联关系的主子订单结构):

请求体:
    
    
    {
    	"content": "{\"orders_num\":$REF{num},\"tid\":\"$REF{tid}\",\"orders\":[$FUNC{mock_all_single($REF{order_param},$REF{num},\\,)}]}",
    	"numb": 1,
    	"function_dic": {
    		"tid": "$FUNC{md5()}",
    		"num": 5,
    		"circular_reference_parse_max_times": 10,
    		"order_param": "{\"content\": \"{\\\"oid\\\": \\\"$FUNC_PRE{md5()}\\\", \\\"tid\\\": \\\"$REF{tid}\\\"}\", \"numb\": 2, \"circular_reference_parse_max_times\": 10}"
    	}
    }


结果(只展示result部分,主订单ID一致,子订单各不相同,外部的子订单个数num字段与实际orders中的子订单个数一致):
    
    
    {
        "orders_num": 5,
        "tid": "2ce0b0f2e34cd6c3796b15dd53594af9",
    	"orders": [{
    		"oid": "b61668137d1b6f863168dfe769dc1209",
    		"tid": "2ce0b0f2e34cd6c3796b15dd53594af9"
    	}, {
    		"oid": "c5f3edcf182b4db2c3a8b5b2c9ff0c7e",
    		"tid": "2ce0b0f2e34cd6c3796b15dd53594af9"
    	}, {
    		"oid": "ca6eab4f0eb7a9ea96d7c049fd898675",
    		"tid": "2ce0b0f2e34cd6c3796b15dd53594af9"
    	}, {
    		"oid": "cd2dd0fc12e2dc683a228d5b0cf921cf",
    		"tid": "2ce0b0f2e34cd6c3796b15dd53594af9"
    	}, {
    		"oid": "89f49ce60dc5996e870d172380fa8d33",
    		"tid": "2ce0b0f2e34cd6c3796b15dd53594af9"
    	}]
    }



     
         
### 安装：
安装：  
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi pydantic faker     
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  uvicorn
```

### 启动：
在api.py目录下执行：
```
uvicorn api:app --port 8001 --host 0.0.0.0 --reload
```

### 结构说明：
```
base目录        -模板处理，将文件解析成可识别函数
func_maker      -函数集，造数据所有的函数都来自这里
api.py          -接口启动文件
```
### 下一步目标(个人水平有限,欢迎各位贡献代码):
* 模板的再封装,将常用功能傻瓜化
* 允许用户上传并执行自定义方法(python文件,jar包等)
* ............


### Get Help:
The fastest way to get response  is to send email to our mail list lisoda@yeah.net , 838331258@qq.com or 879158514@qq.com.
And welcome your advice.  