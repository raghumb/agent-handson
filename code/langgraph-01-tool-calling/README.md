# Tool Calling using Langgraph

# Medium article explaining this. 
[Langgraph: Building a Tool calling agent](https://raghumb.medium.com/langgraph-building-a-tool-calling-agent-e80083b9dc09)

## Setup
- Activate an environment
- pip install -r requirements.txt
- Go to groq.com and register an API key for free.
- Set up env var with the api key. export GROQ_API_KEY=<API_KEY>
- Run streamlit app: streamlit run app/main.py
- Enter a text 'search for hello in /tmp'. If you have some files in /tmp with text 'hello' it will show up.

