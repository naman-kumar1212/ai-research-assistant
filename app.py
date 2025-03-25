from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_tools_agent
from langchain import hub
import os
from dotenv import load_dotenv
import streamlit as st

def initialize_agent():
    # Load environment variables
    load_dotenv()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

    ### Wikipedia Tool
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

    ### WebBaseLoader with custom headers
    loader = WebBaseLoader("https://www.w3schools.com/python/python_classes.asp")
    docs = loader.load()

    ### Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)

    ### Embeddings and Vector Store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = FAISS.from_documents(documents, embeddings)

    ### Retriever Tool
    retriever = vectordb.as_retriever()
    retrieval_tool = create_retriever_tool(retriever, "Python_classes_search", "Search for information about Python Classes")

    ### Arxiv Tool
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

    ### Tools List
    tools = [wiki, arxiv, retrieval_tool]

    ### LLM
    llm = ChatOllama(model="llama3.2")

    ## Get the prompt from hub
    prompt = hub.pull("hwchase17/openai-functions-agent")

    ### Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# App title and description
st.title("AI Research Assistant")
st.markdown("""
This tool helps you research topics using multiple sources:
- Wikipedia for general knowledge
- arXiv for scientific papers
- W3School website information
""")

# Initialize session state to store the agent and conversation history
if 'agent' not in st.session_state:
    with st.spinner('Initializing AI agent...'):
        st.session_state.agent = initialize_agent()
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input("Ask me anything...")

# Process the query when submitted
if user_query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            message_placeholder = st.empty()
            # Run the agent
            response = st.session_state.agent.invoke({"input": user_query})
            result = response.get("output", "I couldn't find an answer to that question.")
            
            # Update the placeholder with the response
            message_placeholder.markdown(result)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})

# Add sidebar with additional options
with st.sidebar:
    st.header("Options")
    
    st.subheader("About")
    st.markdown("""
    This application uses:
    - LangChain for agent orchestration
    - Ollama for local LLM inference
    - Wikipedia API for general knowledge
    - arXiv API for scientific papers
    - Custom knowledge base for W3School
    """)
    
    # Add a button to clear the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
