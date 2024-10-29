from langchain.docstore.document import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from operator import itemgetter
from app.config import DATABASE_URL

embeddings = OpenAIEmbeddings()
store = PGVector(collection_name="mydatabase", connection_string=DATABASE_URL, embedding_function=embeddings)
store.add_documents([Document(page_content="Pizza Margherita costs 5 dollars")])
retriever = store.as_retriever()

template = """
Answer the question based only on the following context:
{context}

Always speak to the user with his/her name: {name}. Never forget the user's name. Say Hello {name}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model_name="gpt-4o-mini")

chain = (
    {"context": itemgetter("question") | retriever, "question": itemgetter("question"), "name": itemgetter("name")}
    | prompt
    | model
    | StrOutputParser()
)
