"""
测试MakeMore包是否安装成功
"""
from MakeMore import MakeMoreAgent
import asyncio

async def main():
    # 配置LLM参数
    llm_configs = {
        "temp": 0.7,
        "topp": 0.9,
        "model_name": "Chat",
        "base_url": "http://111.31.225.50:12811/v1",
        "key": "EMPTY",
        "stop_words": []
    }
    
    # 系统提示词
    system_prompt = """你是一个专业的助手，能够回答各种问题。"""
    
    print("初始化MakeMoreAgent...")
    try:
        # 初始化MakeMoreAgent
        agent = MakeMoreAgent(llm_configs, system_prompt)
        print("初始化成功！")
        
        # 发送简单查询
        print("\n发送测试查询...")
        result = await agent.chat("你好，请简单介绍一下自己。")
        print(f"查询结果: {result}")
        print("\nMakeMore包安装成功并正常工作！")
    except Exception as e:
        print(f"出现错误: {e}")
        print("MakeMore包安装可能存在问题。")

if __name__ == "__main__":
    asyncio.run(main()) 