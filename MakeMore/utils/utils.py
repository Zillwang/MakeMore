# import qianfan
import inspect
import os
import re
import time
from typing import Dict, List, Any
from typing import Dict, List, Any, Tuple
import json
import re

def cal_time(description,return_time=False):
    if return_time:
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                async def wrapper(*args, **kwargs):
                    start_time = time.perf_counter()
                    result = await func(*args, **kwargs)
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time
                    print(f"{description} runs {elapsed_time:.4f} sec")
                    return (*result, elapsed_time) if isinstance(result, tuple) else (result, elapsed_time)
            else:
                def wrapper(*args, **kwargs):
                    start_time = time.perf_counter()
                    result = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time
                    print(f"{description} runs {elapsed_time:.4f} sec")
                    return (*result, elapsed_time) if isinstance(result, tuple) else (result, elapsed_time)
            return wrapper
    else:
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                async def wrapper(*args, **kwargs):
                    start_time = time.perf_counter()
                    result = await func(*args, **kwargs)
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time
                    print(f"{description} runs {elapsed_time:.4f} sec")
                    return result
            else:
                def wrapper(*args, **kwargs):
                    start_time = time.perf_counter()
                    result = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time
                    print(f"{description} runs {elapsed_time:.4f} sec")
                    return result
            return wrapper
    return decorator




def extract_and_parse_json(json_string):
    try:
        # 修改正则表达式，使用 DOTALL 以匹配跨多行的 JSON 对象
        json_match = re.search(r'\{.*\}', json_string, re.DOTALL)
        
        if json_match:
            # 提取匹配到的 JSON 子字符串
            json_part = json_match.group(0)
            
            # 将 JSON 部分解析为 Python 字典
            parsed_dict = json.loads(json_part)
            return parsed_dict
        else:
            print(json_string)
            return {"error": "No valid JSON found in the string"}
    
    except json.JSONDecodeError as e:
        # 捕获 JSON 解析错误并返回错误信息
        return {"error": f"Invalid JSON format: {e}"}

# 示例使用
mixed_str = '''{
    "Thought": "询问中国的四大发明，这是一个常识问题，可以直接回答",
    "Action": "",
    "Action_input": []
}'''

result = extract_and_parse_json(mixed_str)


