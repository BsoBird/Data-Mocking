# Data-Processer

## 简介

##### 1、Data-Processer是什么？

  他是一个模拟数据生成器。我们在测试过程中，产生完整、全面的真实数据可能比较困难。
  我们可以根据需求，创建对应的模版和词典，利用数据模拟生成器生成我们需要的模拟数据。

##### 2、Data-Processer能做什么？

  他能够根据构建的模版和词典，生成我们需要的数据。kafka需要的数据，hive中文件存储数据，接口中JSON数据等等，只要有数据格式，都可以设置成需要的模板。

##### Data-Processer三个应用场景：

*   测试场景

    测试过程中，我们需要验证数据后端的功能或性能，此时，需要降低与数据产生端的耦合，那么需要一个稳定优秀的数据生成器，来持续的不间断的产生正确的数据，和特殊情况下的异常数据。

*   持续集成场景

    在整个持续集成场景中，一个或多个模块组成一个平台，需要有源源不断的数据进入持续集成环境，用以自动化地完成测试和迭代工作，使用Data-Processer则可以通过数据样本的指定和简单的编码，非常简单地完成这个需求。

*   生产场景

    在一个项目完成测试和迭代，发布到生产环境之后，通常也需要进行持续的功能或可用性监测，那么则需要有各种正常或异常数据按照某种规则和定义，持续稳定地生产并送回平台，此时将持续集成场景中的case，只需通过简单配置，则可以进行生产的验证，以满足这个需求。

##### 3、架构

  数据生成器包括：模版变量提取，模版变量执行，模版变量替换三部分组成.

##### 4、术语：

*   函数变量:模版和词典中以`$FUNC{`开头,以`}`结尾的字符串是一个函数变量.形如：`$FUNC{intRand()}`. 其中,intRand()为内置函数. 支持函数嵌套.
*   模板变量：模版中以`$REF{`开头，以`}`结尾的字符串是一个词典变量。形如：`$REF{name}`,其中，name为词典中的一个词典名。
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

##### 6、怎么用？

请使用post请求:  
- `http://host:port/mockData`  产生N条不相同的数据
- `http://host:port/mockData/allsame`  产生N条完全相同的数据

下面是一个DEMO演示.  

body：

    {
        content:"INSERT INTO table_name (name,age,dateTime) VALUES ('$FUNC{name($REF{p1})}', $FUNC{age()},'$FUNC{dateTimeNow()}')",
        numb: 5,
        function_dic:"{p1:$FUNC{name()}}"
    }
    

response:

    {
        result: [
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 23,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 20,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 39,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27,'2020-07-31 00:35:55')"
        ],
        num: 5,
        dateTime:"2020-07-31 00:35:55"
    }

请求参数描述如下:  

*   `content` 待替换的模板
*   `numb` 一次生成多少条数据,一次生成不能超过1W条
*   `function_dic` 模板方法列表,模板方法可以保证在一次mock数据的过程中,同样的模板生成的值始终相同.
 该参数可缺省,若缺省该参数,则不执行模板替换.若传入了该参数,但是传入的字典中没有`content`中出现的待替换的模板,则异常.目前暂不支持模板方法之间相互引用(循环引用问题).