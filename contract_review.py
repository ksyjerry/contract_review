import openai
import PyPDF2
import streamlit as st
import time


openai.api_key = st.secrets["api_secret"]

st.title('Assurance DA')
st.header('AI Game Changer - Document Genius')
st.markdown("<div style='text-align: right;'>Developed by Assurance DA (문의 : <a href = \"mailto:jae-dong.kim@pwc.com\">jae-dong.kim@pwc.com</a>)</div>", unsafe_allow_html=True)
st.write("")
st.markdown("<br>", unsafe_allow_html=True)


# 라디오 버튼을 사용하여 토글 버튼 생성
option = st.radio(
    "언어모델을 선택하세요",
    ("GPT4", "GPT3.5")
)
st.write("GPT4는 성능이 좋으나 느리며 약 7페이지만 가능합니다. GPT3.5는 성능이 다소 떨어지나 빠르며 약 14페이지까지 가능합니다.")

# 선택된 옵션에 따라 메시지 출력
if option == "GPT4":
    llm_model = 'gpt-4'
    n_page = 7
else:
    llm_model = 'gpt-3.5-turbo-16k'
    n_page = 14

st.write('문서를 업로드하고 무엇이든 물어보세요!')



pdf_file = st.file_uploader("파일을 선택하세요(PDF만 가능)", type = ['pdf'])

def get_text():
    input_text = st.text_input('계약서에 대하여 무엇이 궁금하신가요? ' , key ='input')
    return input_text

def chatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
            model = llm_model,
            messages = conversation
            
    )


    conversation.append({'role':response.choices[0].message.role, 'content':response.choices[0].message.content})
    return conversation





# file_name = '게임 (도급) 표준계약서.pdf'


if pdf_file is not None:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    n=0
    page_obj = []
    for page in range(len(pdf_reader.pages)):
        n +=1
        page_obj.append(pdf_reader.pages[page].extract_text())
        

# pdf_file.close()




    conversation = []
    conversation.append({'role':'system','content':'다음 문서를 읽고 묻는 질문에 답변을 기재하고 답변을 찾을 수 있는 조항을 문장 마지막에 괄호안에 알려줘: '})
#     conversation.append({'role':'system','content':'다음 단어가 나오면 이렇게 번역해줘 non-cancellable period - 해지불능기간, lessee - 리스이용자, lessor - 리스제공자: '})
    # conversation = chatGPT_conversation(conversation)

    for i in range(min(n,n_page)):
        conversation.append({"role": "system", "content": page_obj[i]})
        # conversation = chatGPT_conversation(conversation)

    # print(conversation)

#     k=0

    


    # 사용자의 입력 받기
    user_msg = st.text_input('문서에 대하여 무엇이 궁금하신가요?')

    # 사용자의 입력이 있는 경우
    if st.button('질문 제출'):
        conversation.append({"role":"user","content":user_msg})
        conversation = chatGPT_conversation(conversation)
        answer = conversation[-1]['content']
        st.info(answer)

#     else:
#         time.sleep(120)






    # while True:
    #     k+=1
    #     user_msg = st.text_input('계약서에 대하여 무엇이 궁금하신가요? ' , key ='input'+str(k))
    #     if user_msg:

            
    #         conversation.append({"role":"user","content":user_msg})
    #         conversation = chatGPT_conversation(conversation)

    #         answer = conversation[-1]['content']
    #         st.write(answer)









          
    



