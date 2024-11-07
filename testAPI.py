from openai import OpenAI
# 我的版本是：Version: 1.51.2

# alibaba api
client = OpenAI(
    # 输入转发API Key
    api_key="sk-key",
    base_url="http://localhost:9090/v1"
)

# baidu api
# client = OpenAI(
#     # 输入转发API Key
#     api_key="sk-key",
#     base_url="http://localhost:9090/v1"
# )

completion = client.chat.completions.create(
    # 测试不通过：o1-preview-ca、o1-mini-ca 原因可能是调发不一样，请自行参考openai官方文档。因为用Chatbox调用都是可以的
    # 测试通过：gpt-3.5-turbo 、gpt-4o-2024-08-06
    model="llama_3_70b", # gpt-3.5-turbo、gpt-4o-2024-08-06、gpt-4o-ca
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "introduce the large language model behind you in english including the company created it and your nationality. The introduction cannot exceed 70 words. "}
    ],
    stream=False  # 是否开启流式输出
)

# 非流式输出获取结果
print(completion.choices)
