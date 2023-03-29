import openai
import streamlit as st


openai.api_key = st.secrets["api_secret"]

# gpt-3.5-turbo
# gpt-4

st.title('Assurance DA')
st.header('AI Game Changer - Smart Translator')

# st.markdown("<div style='text-align: right;'>Developed by Assurance DA (문의 : <a href = \"mailto:jae-dong.kim@pwc.com\">jae-dong.kim@pwc.com</a>)</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


terms = st.text_area('번역에 사용할 용어를 입력해주세요.', height=100, placeholder ='금융자산 : financial asset \n금융부채 : financial liability')
article_text = st.text_area('번역할 문장을 입력해주세요.', height=300, placeholder ='1500문자 이내로 입력')
lang = st.radio("번역문으로 반환될 언어를 선택해주세요",  ('국문', '영문', '중문','일문','프랑스어','스페인어'))
choice = st.radio("번역 스타일을 설정해주세요",  ('비즈니스 어체', '격식있는 어체', '캐주얼 어체','계약서 번역'))


if lang =='국문':
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in Korean using following terms" 
elif lang=='중문':
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in Chinese Mandarin using following terms" 
elif lang=='일문':
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in Japanese using following terms" 
elif lang=='프랑스어':
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in French using following terms" 
elif lang=='스페인어':
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in Spanish using following terms" 
else:
    order = "You are an accounting and legal expert. Please translate every sentence in the following paragraphs in English using following terms" 

if choice =='비즈니스 어체':
    method = "Please translate them into business language."
elif choice=='격식있는 어체':
    method = "Please translate them into formal language."
elif choice=='캐주얼 어체':
    method = "Please translate them into casual language."
else:
    method = "The following paragraphs are a business contract. When you translate, try your best to make it business formal contract as much as you can"

    
if len(article_text) >1500:
    st.warning('좀 더 짧은 텍스트를 입력해주세요')

else:
    if st.button('번역문 생성하기'):
        completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": order},
        {"role": "system", "content": method},
        {"role": "system", "content": terms},
        {"role": "user", "content": article_text}

            ]
        )
        answer = completions.choices[0]['message']['content']
        st.info(answer)
