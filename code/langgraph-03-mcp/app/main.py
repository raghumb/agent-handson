import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import get_agent_sync
import asyncio

# --- Streamlit UI ---
st.set_page_config(page_title="Stock Agent", page_icon="🔍")
st.title("📂 Stock Agent")
st.caption("Ask me to provide near real time value of a stock.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "agent" not in st.session_state:
    st.session_state.agent = get_agent_sync()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Provide me current stock price of Oracle..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invoke LangGraph Agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # We pass the full history to the agent if needed, 
            # or just the current message for a simple ReAct loop
            response = asyncio.run(st.session_state.agent.ainvoke({"messages": [HumanMessage(content=prompt)]}))
            
            if response:
                # Look for tool calls in the message history
                for msg in response["messages"]:
                    # ToolMessage holds the actual output from your Python function
                    if msg.__class__.__name__ == 'ToolMessage':
                        st.write(f"🔍 Tool Output (Raw): {msg.content}")
                        st.write(f"🆔 Tool Call ID: {msg.tool_call_id}")
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for call in msg.tool_calls:
                            with st.expander(f"🛠️ Tool Call: {call['name']}"):
                                st.json(call['args']) # Displays args in a nice formatted block
            
                # The last message in the response will be the AI's final answer
                final_answer = response["messages"][-1].content
                st.markdown(final_answer)
                
                # Add assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": final_answer})