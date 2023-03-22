import openai
import streamlit as st


openai.api_key = st.secrets["api_secret"]

# gpt-3.5-turbo
# gpt-4

st.title('Assurance DA')
st.header('AI Game Changer - 스마트번역')

st.markdown("<div style='text-align: right;'>Developed by Assurance DA (문의 : <a href = \"mailto:jae-dong.kim@pwc.com\">jae-dong.kim@pwc.com</a>)</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


terms = st.text_area('번역에 사용할 용어를 입력해주세요.', height=100, placeholder ='금융자산 : financial asset \n금융부채 : financial liability')
article_text = st.text_area('번역할 문장을 입력해주세요.', height=300, placeholder ='1500문자 이내로 입력')
lang = st.radio("번역문으로 반환될 언어를 선택해주세요",  ('국문', '영문', '중문','일문','프랑스어','스페인어'))


if lang =='국문':
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in Korean using following terms" +article_text
elif lang=='중문':
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in Chinese Mandarin using following terms" +article_text
elif lang=='일문':
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in Japanese using following terms" +article_text
elif lang=='프랑스어':
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in French using following terms" +article_text
elif lang=='스페인어':
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in Spanish using following terms" +article_text
else:
    order = "You are an accounting expert. Please translate every sentence in the following paragraphs in English using following terms" +article_text

if len(article_text) >1500:
    st.warning('좀 더 짧은 텍스트를 입력해주세요')

else:
    if st.button('번역문 생성하기'):
        completions = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": order},
        # {"role": "system", "content": "결제일 회계처리방법:settlement date accounting \n 실무적 간편법: practical expedient \n 후속적으로 상각후원가로 측정하는 자산: an asset that is subsequently measured at amortised cost"},
        {"role": "system", "content": terms},
        {"role": "user", "content": article_text}

            ]
        )
        answer = completions.choices[0]['message']['content']
        st.info(answer)
