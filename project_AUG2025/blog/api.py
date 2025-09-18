import openai

openai.api_key = "발급받은_API_KEY"
# api key는 환경변수로 바꾸자 

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 여행사 블로그 글 작성 전문가입니다."},
        {"role": "user", "content": "제주도 3박 4일 패키지 여행 블로그 글 작성해줘"}
    ]
)

print(response["choices"][0]["message"]["content"])
