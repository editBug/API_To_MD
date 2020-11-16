import requests
import json


def sendGetRequest(url, headers, params):
    try:
        params = json.loads(params)
        if headers:
            headers = json.loads(headers)
            response = requests.get(url=url, params=params, headers=headers).text
        else:
            response = requests.get(url=url, params=params).text
        return response
    except BaseException as e:
        print('sendGetRequest error:', e)
        return 'Error!'

def sendPostRequest(url, headers, data):
    try:
        data = json.loads(data)
        if headers:
            headers = json.loads(headers)
            response = requests.post(url=url, json=data, headers=headers).text
        else:
            response = requests.post(url=url, json=data).text
        return response
    except BaseException as e:
        print('sendPostRequest error:', e)
        return json.dumps({"Response": "Error!"})


def formatJson(json_data):
    json_dict = json.loads(json_data)
    format_json_data = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    return format_json_data

def analysisDict(data):
    res_dict = {}

    def childFunc(data):
        if isinstance(data, dict):
            for key, value in data.items():
                res_dict[key] = str(type(value)).split("'")[1]
                childFunc(data=value)
        if isinstance(data, list):
            for i in data:
                childFunc(data=i)
        if isinstance(data, int):
            return type(data)
        if isinstance(data, float):
            return type(data)
        if isinstance(data, str):
            return type(data)
        if isinstance(data, bool):
            return type(data)

    childFunc(data)
    return res_dict

# Json -> MD table
def makeMDTable(data):
    table_dict = analysisDict(data)
    len_key = 0
    for i in table_dict.keys():
        len_key = len(i) if len(i) > len_key else len_key

    title_1 = '参数'
    title_2 = '类型'
    title_3 = '说明'
    sep_line = '-'
    md_table_data = f'''| {title_1.ljust(len_key)} | {title_2.ljust(5)} | {title_3.ljust(20)} |
| {sep_line.ljust(len_key, '-')} | {sep_line.ljust(5, '-')} | {sep_line.ljust(20, '-')} |'''
    for key, value in table_dict.items():
        md_table_line = f'''\n| {key.ljust(len_key)} | {value.ljust(5)} | {''.ljust(20)} |'''
        md_table_data += md_table_line
    return md_table_data

# 生成接口文档
def makeMD(request_type, url, headers, data, response):
    # print(request_type, url, headers, data, response)
    request_table = makeMDTable(data=json.loads(data))
    try:
        response = json.loads(response)
    except:
        response = {'response': response}
    response_table = makeMDTable(data=response)
    if headers and headers != '{"headers": "None"}':
        headers_table = makeMDTable(data=json.loads(headers))
        headers_md = f'''
**Headers:** \n
{headers_table}\n
```json
{formatJson(headers)}
```\n'''
    else:
        headers_md = ''
    md_data = f'''
接口地址：{url}
请求方式：{request_type}
请求数据类型：Json
{headers_md}
**请求参数：**\n
{request_table}

```json=
{formatJson(data)}
```

**返回结果：**\n
{response_table}

```json=
{formatJson(response)}
```
'''
    # print(md_data)
    return md_data

