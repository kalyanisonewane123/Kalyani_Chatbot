import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os 

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

def main():

    st.title("Groq Chat App")

    # Add customization options to the sidebar
    
    model = "llama-3.1-70b-versatile"

    conversational_memory_length = 20

    memory=ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})


    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model, temperature=0.4
    )

    conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
    )
       
    if st.button("Generate"):

        if user_question:
            response = conversation(user_question)
            message = {'human':user_question,'AI':response['response']}
            st.session_state.chat_history.append(message)
            st.write("Chatbot:", response['response'])

if __name__ == "__main__":
    main()