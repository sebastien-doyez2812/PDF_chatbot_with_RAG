import argparse
from embedding import get_embedding_function
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama


CHROMA = "chroma"
NB_CONTEXTS = 5

PROMPT = """
Answer the question based only on this following context:
{context}

Answer the question based on the above context:{question}

"""



def main():

    # To get the query text (from the argument arg1 (python main.py arg1))
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help= "This is the query text")
    args = parser.parse_args()

    query_text = args.query_text
    query(query_text)



def query(query_text:str):
    embd = get_embedding_function()
    db =  Chroma(persist_directory = CHROMA, embedding_function= embd)

    results = db.similarity_search_with_score(query_text, k=NB_CONTEXTS)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    #print(context_text)


    prompt_template = ChatPromptTemplate.from_template(PROMPT)
    prompt = prompt_template.format(context=context_text, question= query_text)

    model = Ollama(model="gemma")
    rep = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {rep}\nSOurces:{sources}"
    print(formatted_response)
    return rep

if __name__ == "__main__":
    main()