import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def get_best_model(user_prompt) -> str:
    router_prompt = f"""
    사용자 질문에 대해서 아래 규칙에 따라 가장 적합한 모델을 하나만 선택하세요.

    [선택 기준]
    - gpt-5-nano: 초고속·짧은 응답이 가장 중요한 경우
    - gpt-4.1: 사용자 질문이 1,000자 이상 긴 텍스트의 번역/요약 작업인 경우 
    - gpt-4o: 일반적인 질문·대화 등 일상적 작업(기본값)
    - gpt-5-thinking: 코딩/디버깅/알고리즘/시스템 설계, 수학·논리 문제, 제약 많은 계획 수립 등 복잡한 다단계 추론이 필요한 경우
      다음 표현이 하나라도 포함되면 반드시 gpt-5-thinking 선택
      "깊게 생각", "천천히 생각", "심사숙고", "단계별로", "논리적으로", "면밀히", "추론해", "사고 과정을", "자세히 분석"


    출력 형식: 아래 중 정확히 하나만 출력하세요
    gpt-5-nano | gpt-4o | gpt-5-thinking | gpt-4.1
    
    
    <사용자 질문/>
    {user_prompt}
    </사용자 질문>

    """

    response = client.responses.create(
        model="gpt-5-nano",
        input=router_prompt,
        reasoning={"effort": "minimal"},
    )
    
    recommended_model = response.output_text
    return recommended_model



def llm_stream_events(model: str, messages: list):
    if model == "gpt-5-thinking":
        stream = client.responses.stream(
            model="gpt-5",
            input=messages,
            reasoning={"effort": "medium", "summary": "detailed"},
        )
    elif model == "gpt-5-nano":
        stream = client.responses.stream(
            model=model,
            input=messages,
            reasoning={"effort": "minimal"},
        )
    else:
        stream = client.responses.stream(
            model=model,
            input=messages,
        )
    return stream

def main():

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "자동"
    if "messages" not in st.session_state:
        st.session_state.messages = []  
    MODEL_OPTIONS = [
        "자동",
        "gpt-4o",
        "gpt-5-nano",
        "gpt-5-thinking",
        "gpt-4.1",
    ]


    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.write("## 라우팅 에이전트 ")
    with right_col:
        selected_model = st.selectbox(
            "모델 선택",
            MODEL_OPTIONS,
            index=MODEL_OPTIONS.index(st.session_state["openai_model"])
            if st.session_state["openai_model"] in MODEL_OPTIONS else 0,
            help="대화에 사용할 모델을 선택하세요.",
        )
    st.session_state["openai_model"] = selected_model


    for message in st.session_state.messages:
        icon = ":material/network_intelligence:" if message["role"] == "assistant" else ":material/person:"
        with st.chat_message(message["role"], avatar=icon):
            st.markdown(message["content"])

    prompt = st.chat_input("에이전트에게 물어보기")


    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=":material/network_intelligence:"):
            answer_ph = st.empty()
            if st.session_state["openai_model"] == "자동":
                with st.spinner("🤖 모델 선택중"):
                    selected_model = get_best_model(prompt)
                st.toast(f"🎯 모델 선택: **{selected_model}**")
            else:
                selected_model = st.session_state["openai_model"]
           
            if selected_model == "gpt-5-thinking":
                with st.expander("🔎 추론 과정", expanded=False):
                    reasoning_ph = st.empty()
            else:
                reasoning_ph = None

            answer_chunks = []
            reasoning_chunks = []
            stream = llm_stream_events(
                model=selected_model,
                messages=st.session_state.messages,
            )

            with stream as s:
                for event in s:
                    if event.type == "response.reasoning_summary_text.delta":
                        reasoning_chunks.append(event.delta)
                        reasoning_ph.markdown("".join(reasoning_chunks))
                    elif event.type == "response.output_text.delta":
                        answer_chunks.append(event.delta)
                        answer_ph.markdown("".join(answer_chunks))
                s.until_done()
            response_text = "".join(answer_chunks)

        st.session_state.messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()
