# AI Agent using LangChain and Ollama

## Description
This repository contains the code for an AI agent that utilizes **LangChain** and **Ollama** to search for information within PDFs stored in the `docs` folder and provide precise answers to user questions.

The project includes both the **backend** for the AI agent and the **data processing pipeline** to populate the **vector database**.

## Installation & Usage

### Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```
Then store your PDF in the docs folder.


### Running the Application
To start the backend and frontend:
```bash
python main.py
```
This command will launch the backend and serve the frontend.

### Test the Agent:
To test the agent (ideal for TDD), please use:
```bash
pytest test_agent.py
```

### Frontend
A simple HTML page is included in the `www` folder to interact with the AI agent.

## Links
- 📺 **YouTube Tutorial:** [Watch Here](https://www.youtube.com/watch?v=9Na8DO4MnDM&t=7s)
- 💼 **LinkedIn:** [Sébastien Doyez](https://www.linkedin.com/in/s%C3%A9bastien-doyez-042604252/)

---
Enjoy using the AI agent! 🚀

