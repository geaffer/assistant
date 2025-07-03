import openai
import os
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")  # env로부터 바로 불러옴

def analyze_with_gpt(full_text):
    today = datetime.date.today()
    prompt = f"""
📅 다음은 {today} 기준으로 수집된 일정 및 이메일 정보입니다.

내용을 다음 순서로 간결하게 요약하고, 중요도를 기준으로 정리해줘:

1. 오늘의 주요 일정
2. 앞으로 7일간의 중요한 일정
3. 한 달간의 전체 일정 중 주의할 사항
4. 어제 받은 이메일 중 업무 관련 또는 중요한 메일 정리

내용:
{full_text[:3000]}
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
