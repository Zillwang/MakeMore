"""
测试MakeMore包的多模态图片功能和批量处理功能
"""
from MakeMore import MakeMoreAgent
import asyncio
from pprint import pprint
import os

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
    system_prompt = """你是一个专业的图像分析助手，能够准确描述图片内容。"""
    
    # 初始化MakeMoreAgent
    print("初始化MakeMoreAgent...")
    agent = MakeMoreAgent(llm_configs, system_prompt)
    print("初始化成功！")
    
    # 检查图片是否存在
    image_path = "t2.png"
    if not os.path.exists(image_path):
        print(f"错误: 图片 {image_path} 不存在！")
        return
    
    # 单个多模态查询
    print("\n===== 单个多模态查询 =====")
    try:
        print(f"分析图片: {image_path}")
        result = await agent.mm_chat("这张图片是什么？请详细描述。", image_path)
        print("查询结果:")
        pprint(result)
    except Exception as e:
        print(f"多模态查询出错: {e}")
    
    # 批量多模态查询
    print("\n===== 批量多模态查询 =====")
    try:
        mm_queries = [
            {"question": "描述一下这张图片的内容", "image_url": image_path},
        ]*20
        print(f"批量处理 {len(mm_queries)} 个查询...")
        mm_batch_results = await agent.mm_batch_chat(mm_queries, batch_size=20)
        
        for i, result in enumerate(mm_batch_results):
            print(f"\n多模态查询 {i+1}: {mm_queries[i]['question']}")
            pprint(result)
    except Exception as e:
        print(f"批量多模态查询出错: {e}")
    
    # 批量文本查询
    print("\n===== 批量文本查询 =====")
    try:
        text_queries = [
            "什么是计算机视觉？",
        ]*20
        print(f"批量处理 {len(text_queries)} 个文本查询...")
        batch_results = await agent.batch_chat(text_queries, batch_size=20)
        
        for i, result in enumerate(batch_results):
            print(f"\n文本查询 {i+1}: {text_queries[i]}")
            pprint(result)
    except Exception as e:
        print(f"批量文本查询出错: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 