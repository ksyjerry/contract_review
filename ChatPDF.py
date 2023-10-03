__import__('pysqlite3')
import sys
sys.modules['sqlite3']= sys.modules.pop('pysqlite3')


# from dotenv import load_dotenv
# load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
import streamlit as st
import tempfile
import os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text = ""):
        self.container = container
        self.text = initial_text
    def on_llm_new_token(self, token:str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)



st.title('Assurance DA')
st.header('AI Game Changer - Document Ai')
st.markdown("<div style='text-align: right;'>Developed by Assurance DA (문의 : <a href = \"mailto:jae-dong.kim@pwc.com\">jae-dong.kim@pwc.com</a>)</div>", unsafe_allow_html=True)
st.write("")
st.markdown("<br>", unsafe_allow_html=True)
st.write("---")

def pdf_to_document(file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name,file.name)
    with open(temp_filepath,"wb") as f:
        f.write(file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages


uplodated_file = st.file_uploader("PDF파일을 올려주세요")
if uplodated_file is not None:
    pages = pdf_to_document(uplodated_file)



# pdf = r'C:\Users\jkim564\Documents\Ai\ChatPDF\1116 Lease.pdf'
# loader = PyPDFLoader(pdf)
# pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,

        is_separator_regex=False



    )

    texts = text_splitter.split_documents(pages)

    embeddings_model = OpenAIEmbeddings()

    db = Chroma.from_documents(texts, embeddings_model)

    # question = "리스기간은 어떤 항목으로 구성되어 있나요?"
    # question = '''자산이 특정되더라도, 공급자가 그 자산을 대체할 실질적 권리(대체권)를 
    # 사용기간 내내 가지면 고객은 식별되는 자산의 사용권을 가지지 못한다고 하는데 
    # 어떤 조건을 충족해야 공급자의 자산 대체권이 실질적이라고 볼 수 있나?'''
    # question = '리스계약기간이 5년이고 계약 종료 후 3년간 재계약이 가능하다면 리스기간은 몇년이라고 봐야해?'
    question = st.text_input('질문을 입력하세요')
    query = f'하기 질문에 대한 답변과 답변을 찾을 수 있는 조항을 문장 마지막에 괄호 안에 넣어줘. 질문: {question}'
    if st.button('질문하기'):
        with st.spinner('답변을 생성하는 중입니다.'):
            chat_box = st.empty()
            stream_handler = StreamHandler(chat_box)


            llm = ChatOpenAI(model = "gpt-4", temperature=0, max_tokens=4000,streaming=True, callbacks=[stream_handler])


            # retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db.as_retriever(), llm= llm)

            # docs = retriever_from_llm.get_relevant_documents(query = question)

            qa_chain = RetrievalQA.from_chain_type(retriever = db.as_retriever(), llm = llm)
            qa_chain({"query":query})


            # st.write(result['result'])












