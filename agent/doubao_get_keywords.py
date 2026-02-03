from volcenginesdkarkruntime import Ark
import json

# ---------------- 配置区域 ----------------
# 1. 直接把你的 API Key 填在这里（保留引号）
MY_API_KEY = "c9836894-d14d-4ca0-b2e1-52c9b0dcde4a" 

# 2. 把你的接入点 ID (Model ID) 填在这里
MY_ENDPOINT_ID = "doubao-seed-1-6-lite-251015" 
# ----------------------------------------

# 初始化客户端
client = Ark(
    api_key= MY_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def get_crawler_keywords(user_input):
    """
    输入用户需求，返回关键词列表
    """
    print("正在思考如何生成关键词...")
    
    # 定义提示词（Prompt），告诉豆包怎么做
    system_prompt = """
    你是专业的爬虫工程师，擅长社交媒体舆情搜索关键词构建，请根据用户提出的舆情分析需求，生成适配的搜索关键词。
    要求：
    1. 只需要输出一个JSON格式的字符串列表，无其他解释说明及Markdown标记和代码块符号；
    2. 关键词需要覆盖核心词、长尾词，同时包含相关正面、负面情绪词，维度全面且贴合社交媒体生活化搜索场景；
    3. 关键词数量控制在10-15个之间，以英文逗号分隔，需围绕核心主题，确保覆盖用户需求的多个维度。
    4. 关键词应简洁明了，避免使用复杂或冗长的表达。
    示例输出：
    温江 臭味;温江 空气质量差;温江 空气清新；温江区 环境改善
    """

    try:
        # 发送请求（这是纯文本请求）
        completion = client.chat.completions.create(
            model=MY_ENDPOINT_ID, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )

        # 获取AI的回复
        result_text = completion.choices[0].message.content.strip()
        
        # 清理可能残留的markdown符号（以防万一）
        result_text = result_text.replace("```json", "").replace("```", "")
        
        # 将字符串转为Python列表
        keywords = json.loads(result_text)
        return keywords

    except Exception as e:
        print(f"发生错误: {e}")
        return []

# --- 测试运行 ---
if __name__ == "__main__":
    # 模拟用户输入
    requirement = "我想查一下最近一年温江区房屋中介的情况，进行舆情分析，请帮我生成一些适合在社交媒体平台搜索的关键词。"
    
    # 调用函数
    keywords = get_crawler_keywords(requirement)
    
    print("-" * 30)
    print("用户需求:", requirement)
    print("豆包生成的爬虫关键词:", keywords)
    print(\n)
    print("请复制关键词至base_config.py的KEYWORDS配置项中使用")
    print("-" * 30)
    
 