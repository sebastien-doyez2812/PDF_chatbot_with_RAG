import pytest
from langchain_community.llms.ollama import Ollama
from main import query


EVAL_PROMPT_TEMPLATE= """
This is answer1:
{answer_agent}
This is the expected answer:
{expected_answer}

Answer just with True if the answer1 is close to the expected answer. If not, answer False

"""

#############################################
#            TEST Questions                 #
#############################################

ANS1 = "what is deep learning?"
REP1 = "Deep learning is a machine learning technique that uses multiple layers of features to automatically discover representations needed for detection or classification of objects in data. It utilizes a general-purpose learning procedure to learn features from data without human engineering."

#############################################
#                 Test Code                 #
#############################################
@pytest.mark.parametrize("query, expected_res", [(ANS1, REP1)])
def test_agent( query:str, expected_res:str):
    assert(validate_result(query,expected_res))
    
def validate_result(question:str, expected_res:str):
    agent_answer = query(question)
    model = Ollama(model="gemma")
    homogen_res = (model.invoke(EVAL_PROMPT_TEMPLATE.format(answer_agent = agent_answer, expected_answer= expected_res))).lower().strip()
    if homogen_res == "true":
        return True
    elif homogen_res == "false":
        return False
    else:
        raise ValueError("[-] The test LLM did not answer with true or false... ")




#def main():
#    test_agent(ANS1, REP1)


#if __name__ == "__main__":
#    main()