# 라우팅 에이전트

질문 유형에 따라 최적의 OpenAI 모델을 자동으로 선택하는 라우팅 AI 에이전트입니다.   
프롬프트를 분석하여 가장 적합한 모델  
(GPT-4o, GPT-5-nano, GPT-5-thinking, GPT-4.1)로 라우팅하여 최적의 성능을 제공합니다.
<img width="3541" height="1867" alt="image" src="https://github.com/user-attachments/assets/97d5eabf-c375-4b99-8305-acd14796cfb3" />



### GPT 5 모델정보 (API 제공 기준, 25.08 기준)


| 모델 | 주요 용도 |
|------|----------|
| **gpt-5-nano** | **단순 지시 수행, 분류 작업** |
| gpt-5-mini | 일반적인 추론과 대화 |
| gpt-5 | 복잡한 추론, 코딩, 다단계 에이전트 작업 |



### [모델 정보](https://platform.openai.com/docs/models/compare) ('25.08 기준)

| 상황 | 모델 | 입력 (/1M 토큰) | 출력 (/1M 토큰) | 컨텍스트 길이 (토큰) | 속도 | 비고 |
|------|------|-----------------|-----------------|-------------------|------|------|
| 빠른 응답 | GPT-5-nano | $0.05 | $0.40 | 400,000 | ⚡⚡⚡⚡⚡ | 가장 빠른 응답 |
| 일상 | GPT-4o | $2.50 | $10.00 | 128,000 | ⚡⚡⚡ | 균형잡힌 성능, 유연성 |
| 긴 맥락 | GPT-4.1 | $2.00 | $8.00 | 1,047,576 | ⚡⚡⚡ | 가장 긴 컨텍스트 윈도우 |
| 고차원 추론 (코딩 등) | GPT-5-Thinking | $1.25 | $10.00 | 400,000 | ⚡⚡ | 코딩과 에이전트 작업에 최적화 |



## 필수 요구사항

- [uv](https://docs.astral.sh/uv/) 패키지 매니저
- OpenAI API 키

## 설치 방법

1. **레포지토리 복제 또는 다운로드**
2. **[OpenAI API 키 설정](https://github.com/dabidstudio/dabidstudio_guides/blob/main/get-openai-api-key.md)**:  
   `.env` 파일 생성하고 키 입력
   ```bash
   OPENAI_API_KEY=여기에_실제_API_키_입력
   ```

3. 실행
   
   ```bash
   uv run streamlit run main.py
   ```
