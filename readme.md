# Data-Mocking
## background
In the daily development, testing process, we often encounter a variety of strange data creation needs, most of the time we are customised for the needs of the development of mock program, but this program is often not reusable, the development process is also time-consuming and laborious.
and there are some complex scenarios, so that people do not see the desire to write their own code Mock data, such as the following scenarios.
- Generate a large number of xxx with N(N>50) fields, each with certain rule requirements
- Generate a large number of master-child xx with N(N>50) fields, and need to maintain the association relationship
- On the basis of the above, it is extended to multi-level associations and multi-field associations (star model scenario, snowflake model scenario).
- You've got the above scenarios down, and then the requirements change. because odds are you have hard-coded code.
- Blah blah blah ........
Against this background, Data-Mocking was born. Its initial intention is to free us from the complexity of the requirements of the scene, so that the user focuses only on the data model and business logic, to achieve flexible configuration, reduce the workload and improve productivity.

## brief introduction

##### 1. What is Data-Mocking？

  It is a simulated data generator. It may be difficult to generate complete and comprehensive real data during our testing.
  We can create the corresponding templates and dictionaries according to the requirements and use the data simulation generator to generate the simulated data we need.

##### 2. What Data-Mocking can do?

  It can generate the data we need based on the templates and dictionaries we build. kafka data, file storage data in hive, JSON data in interfaces, etc., as long as there is a data format, you can set up the template you need.

##### Three application scenarios for Data-Mocking：

*   **Test scenarios**

    Testing process, we need to verify the functionality or performance of the data back-end, at this time, the need to reduce the coupling with the data generating end, then a stable and excellent data generator is needed to continue to uninterruptedly generate the correct data, and special cases of abnormal data.

*   **Continuous Integration Scenarios**

    In a continuous integration scenario, one or more modules form a platform that requires a constant flow of data into the continuous integration environment to automate testing and iteration, which can be accomplished very simply by specifying data samples and simple coding using Data-Mocking.

*   **Prod scenarios**

    In a project to complete the testing and iteration, released to the production environment, usually also need to carry out continuous functionality or usability monitoring, then there is a need for a variety of normal or abnormal data in accordance with certain rules and definitions, continuous and stable production and sent back to the platform, at this time will be a continuous integration scenario of the case, just through a simple configuration, can be verified by the production in order to meet this demand.

##### 3. architecture

  The data generator consists of three parts: template variable extraction, template variable execution, and template variable replacement.

##### 4. term：

* **Function variables**: Strings in templates and dictionaries that begin with `$FUNC{` and end with `}` are function variables. For example: `$FUNC{intRand()}`. Where intRand() is a built-in function. Nested functions are supported.
* **Precompiled function variables**: Strings in templates and dictionaries that begin with `$FUNC_PRE{` and end with `}` are a precompiled function variable. Example: `$FUNC_PRE{intRand()}`. Where intRand() is a built-in function. Nested functions are supported. The pre-compiled function will only take effect when the sub-template is executed, in general he is a string.
* **Template variable**: A string in the template starting with `$REF{` and ending with `}` is a dictionary variable. Shape: `$REF{name}`, where name is the name of a dictionary in the lexicon. Template variables are allowed to reference each other.
 example:`$FUNC{dateStringWithRange($FUNC{long(123456789)},$FUNC{timestamp()},$REF{test_name})}`
* **Pre-compiled template variables**: similar to pre-compiled function variables

##### 5. Built in functions

* **Can call any python basic function, supports pyhton style function passing.**
Example:`$FUNC{name(a=1,b=2)}`

* **eval(str)**
**Expressions that can execute any python statement, or return the original value if they cannot be executed. **
Example:`eval(1+2)`

* **concat(args....)**
Splice the incoming argument list as a string.

* **concat_ws(tag,args...)**
Splits the list of incoming arguments by the specified separator.

* **The methods for arbitrary mock data in the Faker module are detailed in `https://pypi.org/ project/Faker/`.**

* **name(arg=None)** Returns the passed-in value if passed in. Otherwise, name is randomly generated.

* **company(arg=None)**
Get the name of the company, if the parameter is passed in, then return the value passed in, otherwise it will be randomly generated.

* **age(arg=None)**
Get a random age, if you pass in a parameter, return the passed in value, otherwise it will generate a random number within 15~60.

* **Id(arg=None)**
Get a random ID, if you pass in a parameter, return the passed in value, otherwise it will generate a random number within 1111111111111111~9111111111111111.

* **timeNow(arg=None)**
If passed a parameter, it returns the passed value, otherwise it generates the hour, minute and second of the current time.

* **dateNow(arg=None)**
If you pass a parameter, it returns the passed value, otherwise it generates the year, month and day of the current time.

* **dateTimeNow(arg=None)**
If you pass a parameter, it returns the passed value, otherwise it generates the year, month, day, hour, minute and second of the current time.

* **quote_escaped(str_val)**
Escapes unescaped single and double quotes in text.

* **quote_replacement(str_val)**
Escape $ and \ in a string.

* **mock_default(mock_template,exec_times,result_concat_separator)**
We support the use of another template in the template to generate data, this scenario is usually used to generate a nested structure, and there is a correlation between the inner and outer data **. The parameters are described as follows.
    * :: `mock_template`: incoming json template, refer to `Chapter 6` for template content.
    * :: `exec_times` : the number of times the template is executed, if -1 is passed and the `numb` attribute in the template is greater than 0, then `numb` is used.
    * :: `result_concat_separator` : A spacer to perform result concatenation. Since the result must be a string, only the concatenation function is provided.

* **mock_all_single(mock_template,exec_times,result_concat_separator)**
** Close to the `mock_default` method, but it differs from the above in that each execution of the template is independent, ensuring that the same data is not generated**.

##### 6、Basic usage guide

Please use post request:  
- `http://host:port/mockData`  Generate N different pieces of data
- `http://host:port/mockData/allsame`  Generate N identical data

Below is a demo.  

body：

    {
        "content":"INSERT INTO table_name (name,age,dateTime) VALUES ('$FUNC{name($REF{p1})}', $FUNC{age()},'$FUNC{dateTimeNow()}')",
        "numb": 5,
        "function_dic":{"p1":"$FUNC{name()}"}
    }
    

response:

    {
        "result": [
            "INSERT INTO table_name (name,age,dateTime) VALUES ('Kim', 23,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('Kim', 20,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('Kim', 39,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('Kim', 27,'2020-07-31 00:35:55')",
            "INSERT INTO table_name (name,age,dateTime) VALUES ('Kim', 27,'2020-07-31 00:35:55')"
        ],
        "num": 5,
        "dateTime":"2020-07-31 00:35:55"
    }

The request parameters are described as follows:  

*   **`content` Template to be replaced**
*   **`numb` How many pieces of data can be generated at once, and cannot exceed 10000 pieces at a time**
*   **`function_dic` Template method list, can be defaulted**.The template method ensures that the same template will always generate the same value in a single mock. Any legal `content` (string, method ......) is allowed in this list. .
 This parameter can be defaulted, and if it is, no template replacement is performed. If this parameter is passed, but the template to be replaced does not appear in 'content' in the passed dictionary, an exception is thrown. Cross-referencing between template methods is supported. 
*   **`circular_reference_parse_max_times` Maximum number of parsing times for circular references, default to 1, can be defaulted**。Since in `function_dic` we allow template methods to refer to each other, then there is the problem of N templates referencing each other to form circular references.
Since infinite parsing will result in a dead loop, here we make a restriction that the parsing of template references can only be performed N times, and after N times no more parsing will be performed, and the string like `$REF{XXX}` will be returned directly. Since the original string will be replaced every time, it is not guaranteed to return the `$REF{XXX}` string passed to the user.
 ##### 7. Advanced User Guide
 * **Special delimiter**.Sometimes we need to use special delimiters to concatenate strings to produce results, such as building hive data files. Due to the limitations of the python json package, special characters need to be passed the corresponding unicode code. For example, \x01` needs to be written as \u0001`.
 * **Splicing with commas**.Since commas are often used to separate argument lists during function parsing, and many times we want to use commas to splice the contents, we handle this by passing in \, \ to identify the functions \cat_ws`, \mock_default`, and \mock_all_single` (see example for details).
 * **The use of blank spaces**.Because in the internal implementation, all the methods are trimmed once, if you want to implement a function like splicing a blank character into a string, like `concat(' ','a')`, you can't use Function to implement it directly.
 But can be slightly modified, we can take the form of this way to achieve `$FUNC{t1()} $FUNC{t2()}`, in the template to leave a blank, so you can disguise the implementation of the function
 * **Template Method List**.For too complex template fragments, it can be written into the template method list, in the main template to refer to the fragment can be, but after doing so, the batch of data generated by the referenced template method will generate the exact same data, if you want to generate different data, you need to call multiple times.  
 * **Guidelines for using sub templates**. We support the use of the `mock_default` and `mock_all_single` methods to generate data through sub-templates and use the results in the main template. **Typically, sub-templates are designed to handle mock nested data with associative relationships. If you need to generate non-nested data with associative relationships, the current version requires the user to first make it nested, and then split it up outside.**
 For sub-templates, since they can be complex, it is best to include them in the list of template methods. The use of sub-templates requires the following attention:
     * Since the whole template engine execution process, is in accordance with the `Execute template method list` -> `Execute template method list execution results to replace the main template` -> `Execute template appearing in the method (top-down LL)` -> `Execute the method results to replace the template` such a sequence of execution. If a method exists in a sub-template, it will be executed first, and the sub-templates may end up executing exactly the same result. To avoid this, function definitions in sub-templates should use `$FUNC_PRE{`.
     **Implementation**: `$FUNC_PRE{` will not trigger the method execution, so it is guaranteed that strings like `$FUNC_PRE{xxx}` can be passed into the method as it is, and `$FUNC_PRE{` will be replaced by `$FUNC` in the `mock_default` and `mock_all_single` methods so that the sub-templates can trigger the method execution again. method execution is triggered again by executing the sub-template.
     * If there is a method reference in the sub-template, the following situation exists:
         * The presence of pre-compiled method references in a sub-template ensures that the sub-template will use its own template variables.
         * If the parent template's circular reference resolution is large enough, it will use the parent template's list of template methods to replace them, not its own, and thus recursively work its way down (if your child template also has a child template).
         * If the parent template's circular reference resolution is not large enough, the `$REF{xxx}` string in the child template will not be cleanly replaced, and then the child template's method references will be used in the execution of the mock method, **but this method is less controllable than the previous one, and requires absolute certainty on the part of the user**.


`Example`(Generate a nested structure with a primary and secondary order structure that is related both internally and externally):

request body:
    
    
    {
    	"content": "{\"orders_num\":$REF{num},\"tid\":\"$REF{tid}\",\"orders\":[$FUNC{mock_all_single($REF{order_param},$REF{num},\\,)}]}",
    	"numb": 1,
    	"circular_reference_parse_max_times": 10,
    	"function_dic": {
    		"tid": "$FUNC{md5()}",
    		"num": 5,
    		"order_param": "{\"content\": \"{\\\"oid\\\": \\\"$FUNC_PRE{md5()}\\\", \\\"tid\\\": \\\"$REF{tid}\\\"}\", \"numb\": 2, \"circular_reference_parse_max_times\": 10}"
    	}
    }


Result (only the result section is displayed, with the main order ID consistent and each sub order different. The number of external sub orders in the num field is consistent with the actual number of sub orders in the orders):
    
    
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



     
         
### install：
install:  
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi pydantic faker     
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  uvicorn
```

### start-up：
```
uvicorn api:app --port 8001 --host 0.0.0.0 --reload
```

### Structural Description：
```
base directory  -Template processing, parsing files into recognizable functions
func_maker      -function list
api.py          -start-up
```


### Get Help:
The fastest way to get response  is to send email to our mail list plashspeed@foxmail.com.
And welcome your advice.  
