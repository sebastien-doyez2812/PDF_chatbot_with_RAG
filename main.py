"""
Author: Sébastien Doyez
date: 10/02/2025
"""

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma



DATA_PATH = "C:/Users/doyez/Documents/PDF_chatbot_with_RAG/docs/"
CHROMAPATH = "chroma"



def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings



def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function=len,
        is_separator_regex = False
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks:list[Document]):
    db = Chroma(persist_directory=CHROMAPATH,
                embedding_function= get_embedding_function())
    db.add_documents(new_chunks, ids = new_chunks_ids)
    db.persist()
    ###### to finish

def calculate_id_chunk(chunk):
    page_id = 0
    idx_chunk = 