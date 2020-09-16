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

### 使用：
启动后是post请求:`http://host:port/mockData`

body：
```json
{
    "content": "INSERT INTO table_name (name,age,dateTime) VALUES ('$FUNC{name($REF{p1})}', $FUNC{age()}, '$FUNC{dateTimeNow()}')",
    "numb": 5,
    "function_dic":{"p1":"$FUNC{name()}"}
}
```
response:
```json
{
    "result": [
        "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 23, '2020-07-31 00:35:55')",
        "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 20, '2020-07-31 00:35:55')",
        "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 39, '2020-07-31 00:35:55')",
        "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27, '2020-07-31 00:35:55')",
        "INSERT INTO table_name (name,age,dateTime) VALUES ('梁强', 27, '2020-07-31 00:35:55')"
    ],
    "num": 5,
    "dateTime": "2020-07-31 00:35:55"
}
```