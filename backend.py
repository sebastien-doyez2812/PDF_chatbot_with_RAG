import argparse
from embedding import get_embedding_function
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from flask import Flask, request, jsonify
from flask_cors import CORS


CHROMA = "chroma"
NB_CONTEXTS = 5

PROMPT = """
Answer the question based only on this following context:
{context}

Answer the question based on the above context:{question}

"""

app = Flask(__name__)
CORS(app)

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
    #formatted_response = f"Response: {rep}\nSOurces:{sources}"
    #formatted_response = {"response":rep, "sources": sources}
    
    
    formatted_response = {
    "response": rep,
    "sources": sources if sources else []  # Toujours un tableau
    }

    print(f"\n\n_____\n\n{formatted_response}")
    return rep



@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question","")

    if not question.strip():
        return jsonify({"error": "Empty question"}), 400

    response = query(question)
    print("\n\n\nvoici la réponse", jsonify(response))
    return jsonify(response)

if __name__ == "__main__":
    #main()
    app.run(host="0.0.0.0", port = 5000, debug=True)