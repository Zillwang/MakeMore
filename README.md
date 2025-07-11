# MakeMore

MakeMore是一个灵活的AI助手工具，支持文本和图片API调用。

## 安装

```bash
pip install make-more -e
```

## 快速开始

### 基本使用

```python
from MakeMore import MakeMoreAgent
import asyncio

async def main():
    # 配置LLM参数
    llm_configs = {
        "temp": 0.7,
        "topp": 0.9,
        "model_name": "Chat",
        "base_url": "你的API地址",
        "key": "你的API密钥",
        "stop_words": []
    }
    
    # 系统提示词
    system_prompt = """你是一个专业的助手，能够回答各种问题。"""
    
    # 初始化MakeMoreAgent
    agent = MakeMoreAgent(llm_configs, system_prompt)
    
    # 发送查询
    result = await agent.chat("上海有哪些著名的景点？")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 批量查询

```python
# 批量文本查询
queries = [
    "北京的著名美食有哪些？",
    "杭州西湖的十景是什么？",
    "成都的特色是什么？"
]
batch_results = await agent.batch_chat(queries, batch_size=3)
```

### 多模态查询

```python
# 多模态查询（带图片）
mm_result = await agent.mm_chat("这张图片是什么？", "path/to/image.jpg")

# 批量多模态查询
mm_queries = [
    {"question": "描述一下这张图片", "image_url": "path/to/image1.jpg"},
    {"question": "这张图片中有什么物体？", "image_url": "path/to/image2.jpg"}
]
mm_batch_results = await agent.mm_batch_chat(mm_queries, batch_size=2)
```

## 功能特点

- 支持文本查询和多模态查询
- 支持批量处理请求
- 异步处理，提高效率
- 简单易用的API

## 许可证

MIT 
