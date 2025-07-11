from MakeMore.make_more import MakeMoreAgent
import asyncio
from pprint import pprint

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
    
    # 初始化MakeMoreAgent
    agent = MakeMoreAgent(llm_configs, system_prompt)
    
    # 单个文本查询示例
    print("===== 单个文本查询 =====")
    result = await agent.chat("上海有哪些著名的景点？")
    pprint(result)
    
    # 批量文本查询示例
    print("\n===== 批量文本查询 =====")
    queries = [
        "北京的著名美食有哪些？",
        "杭州西湖的十景是什么？",
        "成都的特色是什么？"
    ]
    batch_results = await agent.batch_chat(queries, batch_size=3)
    for i, result in enumerate(batch_results):
        print(f"\n查询 {i+1}: {queries[i]}")
        pprint(result)
    
    # 多模态查询示例（如果有图片）
    try:
        print("\n===== 多模态查询 =====")
        mm_result = await agent.mm_chat("这张图片是什么？", "data/output/sample.jpg")
        pprint(mm_result)
    except Exception as e:
        print(f"多模态查询出错: {e}")
    
    # 批量多模态查询示例
    try:
        print("\n===== 批量多模态查询 =====")
        mm_queries = [
            {"question": "描述一下这张图片", "image_url": "data/output/sample1.jpg"},
            {"question": "这张图片中有什么物体？", "image_url": "data/output/sample2.jpg"}
        ]
        mm_batch_results = await agent.mm_batch_chat(mm_queries, batch_size=2)
        for i, result in enumerate(mm_batch_results):
            print(f"\n多模态查询 {i+1}: {mm_queries[i]['question']}")
            pprint(result)
    except Exception as e:
        print(f"批量多模态查询出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())
