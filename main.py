"""
Author: Sébastien Doyez
date: 10/02/2025
"""

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader


DATA_PATH = "C:/Users/doyez/Documents/PDF_chatbot_with_RAG/docs/"

def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


doc = load_documents()
print(doc[0])
