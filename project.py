# Requirements
# Load any PDF of your choice — research paper, textbook chapter, documentation
# Smart index — checks if index exists, loads from disk, else builds and saves
# Answer ONLY from the document — "I don't know" for anything outside
# Source citations after every answer — page number, source file, first 100 chars, similarity score
# Conversation memory — follow-up questions work correctly
# Multiple sessions — at least two users with separate histories
# Interactive loop — user types questions until quit
# Session inspector — after the session ends, print full conversation stats using inspect_session()
# Timing — print how long index load/build took

# Bonus: Add a mode selector at the start — user picks "chat" (normal Q&A) or "deep" (uses k=8 for more thorough retrieval). 
# Use RunnableBranch from Week 1 to route between two retrievers.

import os
import json
import time

import warnings
warnings.filterwarnings("ignore")

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableParallel,RunnableBranch
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_ollama import ChatOllama
from operator import itemgetter

loader = PyPDFLoader("Game of thrones.pdf")
chunks = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 300
).split_documents(loader.load())

embeddings = HuggingFaceEmbeddings(
    model_name = "all-MiniLM-L6-v2",
    cache_folder = ".models",
    model_kwargs = {"device":"cpu"},
    encode_kwargs = {"normalize_embeddings":True}
)

INDEX_PATH = "faiss_index"
start = time.time()
if os.path.exists(INDEX_PATH):
    vectorstore = faiss.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization = True
    )
else:
    vectorstore = faiss.from_documents(chunks,embeddings)
    vectorstore.save_local(INDEX_PATH)
end = time.time()

retriever = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {
        "k": 4
    }
)

retriever2 = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {
        "k":8
    }
)

prompt = ChatPromptTemplate.from_messages([
    ("system","""You're a helpful assistant, answer the question that user asks using the context.
        If answer is not in the context, say I don't know. Keep answers concise and accurate."""),
    Messagesplaceholder(variable_name = "chat_history"),
    ("human","{input}")
])

llm = ChatOllama(model = "llama3.2:3b",temperature = 0)

context_chain = itemgetter("input")|retriever
context_chain_2 = itemgetter("input")|retriever2

store = {}
def session_history(session_id:str)->InMemoryChat:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

qa_chain = RunnableParallel(
    input = itemgetter("input"),
    chat_history = itemgetter("chat_history"),
    context = context_chain
)|prompt|llm|StrOutputParser()

deep_chain = RunnableParallel(
    input = itemgetter("input"),
    chat_history = itemgetter("chat_history"),
    context = context_chain_2
)|prompt|llm|StrOutputParser()

branch = RunnableBranch(
    (lambda x: x['mode'].lower().strip() == "chat",qa_chain),
    deep_chain
)

chain_with_memory = RunnableWithMessageHistory(
    branch,
    session_history,
    input_messages_key = "input",
    history_messages_key = "chat_history"
)

def ask(session_id:str,mode:str,question:str)->str:
    result = answer_with_memory.invoke(
        {"input":question},
        config = {"configurable":{"session_id":session_id}}
    )

    print(f"YOU: {question}")
    print(f"BOT: {result}")

if __name__ == "__main__":
    print("----------Get into the world of 'GAME OF THRONES'")
    print("type 'quit' to exit")
    print("Available Modes: \n chat, \n deep")
    while True:
        mode = input("select the mode:")
        if mode in ["chat","deep"]:
            question = input("enter your question:")
            if question.lower() == "quit":
                break
            ask(session_id,mode,question)
        else:
            print("Invalid Mode. Please enter the available modes")