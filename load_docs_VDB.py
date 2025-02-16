"""
Author: Sébastien Doyez
date: 10/02/2025
"""
import argparse
import os
import shutil
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from embedding import get_embedding_function


DATA_PATH = "C:/Users/doyez/Documents/PDF_chatbot_with_RAG/docs/"
CHROMAPATH = "chroma"



def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()





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
    

    chunks_with_ids = calculate_id_chunks(chunks)

    existing_items = db.get(include = [])
    # Create a set: a set contains only uniques values ( no duplicates data!)
    existing_ids = set(existing_items["ids"])
    print(f" There are {len(existing_ids)} existings docs!")

    # Add only the new chunks of data in db
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    if len(new_chunks):
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids= new_chunk_ids)
        db.persist()
        print(f"[+] Adding Documennts done!")

    else:
        print("[i] No new documents...")

def calculate_id_chunks(chunks):
    page_id = 0
    last_page_id = None
    current_chunk_index = 0
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")

        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index +=1

        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id
    return chunks


def clear_db():
    if os.path.exists(CHROMAPATH):
        shutil.rmtree(CHROMAPATH)

def main():

    parser = argparse.ArgumentParser()
    # action = store_true mean if the --reset option is here, 
    # put reset to true...
    parser.add_argument("--reset", action="store_true", help= " Reset the Vector Database" )
    args = parser.parse_args()
    if args.reset:
        print("[i] Clear the database...")
        clear_db()

    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


if __name__ == "__main__":
    main()