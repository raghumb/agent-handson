from llm import get_llm
from langgraph.prebuilt import create_react_agent
import os
from langchain_core.tools import tool


@tool
def search_text_in_files(query: str, directory: str = "."):
    """Searches for a specific string inside all text files within a directory."""
    results = []
    expanded_dir = os.path.abspath(os.path.expanduser(directory))
    try:
        print(expanded_dir)
        for root, _, files in os.walk(expanded_dir):
            for file in files:
                print(file)
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if query.lower().strip() in f.read().lower():
                            results.append(file_path)
                except (UnicodeDecodeError, PermissionError):
                    continue 
        return f"Found '{query}' in: {results}" if results else "No matches found."
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"

# Define the toolset
tools = [search_text_in_files]
llm = get_llm()

# Create the Agent Executor
app = create_react_agent(llm, tools)

# Run a query
def invoke_agent(user_input: dict):
    # user_input should be {"messages": [HumanMessage(...)]}
    '''for s in app.stream(user_input, stream_mode="values"):
        message = s["messages"][-1]
        message.pretty_print()'''
        
    return app.invoke(user_input)


