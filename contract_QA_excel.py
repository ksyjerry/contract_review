import openai
import PyPDF2
import streamlit as st
import pandas as pd
from io import BytesIO


# from io import BytesIO
# from pyxlsb import open_workbook as open_xlsb


openai.api_key = st.secrets["api_secret"]

st.title('Assurance DA')
st.header('AI Game Changer - Vouching Coach')
# st.markdown("<div style='text-align: right;'>Developed by Assurance DA (문의 : <a href = \"mailto:jae-dong.kim@pwc.com\">jae-dong.kim@pwc.com</a>)</div>", unsafe_allow_html=True)
st.write("")
st.markdown("<br>", unsafe_allow_html=True)

st.write('증빙을 업로드하고 무엇이든 물어보세요!')

uploaded_files = None
csv_file = None

engine = st.radio("GPT모델을 선택해주세요",  ('GPT3.5', 'GPT4'))

if engine =='GPT3.5':
    engine_model = "gpt-3.5-turbo"
else:
    engine_model = "gpt-4"

uploaded_files = st.file_uploader("증빙 PDF 파일을 업로드하세요(다수의 파일 가능).", type="pdf", accept_multiple_files=True)
csv_file = st.file_uploader("질문 파일을 선택하세요(csv만 가능 1열 제목, 2열 질문)", type=['csv'])

# gpt-4
# gpt-3.5-turbo

def chatGPT_conversation(conversation_input):
    response = openai.ChatCompletion.create(
            model=engine_model,
            messages=conversation_input
    )

    return response




def ask_question(conversation, content):
    conversation_try = conversation.copy()
    conversation_try.append(
        {
            "role": "user",
            "content": content
        }
    )
    
    answer = chatGPT_conversation(conversation_try)
    
    answer_content = answer.choices[0].message.content

    return answer_content



def convert_df(df):
    file_name = 'summary.xlsx'
    return df.to_excel(file_name, index=False, sheet_name='Sheet1')


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

#    return df.to_csv(index=False).encode('cp949')



if uploaded_files is not None and csv_file is not None:
    

    dataframe = pd.read_csv(csv_file)
    st.subheader('기본 질문 리스트')
    st.write(dataframe.iloc[:,0])
    n=0



  

    # 사용자의 입력이 있는 경우
    if st.button('기본 질문 제출'):
        df_result = dataframe.copy()

        for uploaded_file in uploaded_files:
        
            # PyPDF2 라이브러리를 사용하여 PDF 파일 열기
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            n+=1
            # PDF 파일의 페이지 수
            num_pages = len(pdf_reader.pages)
            conversation = []
            conversation.append(
                {
                    'role': 'system',
                    'content': '다음 문서를 읽고 묻는 질문에 답변을 기재하고 답변을 찾을 수 있는 조항을 문장 마지막에 괄호안에 알려줘: '
                }
            )
            st.subheader(uploaded_file.name)
        # 페이지 수만큼 반복문 돌면서 텍스트 추출
            for page in range(min(4,num_pages)):
                # 페이지 번호에 해당하는 페이지 객체 가져오기
                pdf_page = pdf_reader.pages[page]
                # 페이지 객체에서 텍스트 추출
                text = pdf_page.extract_text().replace("\n", "")
                # 추출된 텍스트 출력
                conversation.append({"role": "system", "content": text})
                # st.info(conversation)

                df_result[uploaded_file.name] = ''

            for i, row in dataframe.iterrows():
                row_title = row[0]
                row_question = row[1]

                st.write(row_title)
                row_answer = ask_question(conversation, row_question)
                df_result.loc[i, uploaded_file.name] = row_answer.strip()

                st.write(row_answer.strip())



        df_xlsx = to_excel(df_result)
        st.download_button(label='결과 파일 다운로드',
                                data=df_xlsx ,
                                file_name= 'df_test.xlsx')


    
