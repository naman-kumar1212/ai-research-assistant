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
    """Initializes and configures the AI agent.

    This function sets up the entire agent by loading environment variables,
    initializing the necessary tools (Wikipedia, Arxiv, and a custom web-based
    retriever), configuring the language model (LLM), and creating an
    agent executor.

    Returns:
        langchain.agents.AgentExecutor: An agent executor instance ready to
        process user queries.
    """
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

def setup_page():
    """Sets up the Streamlit page configuration.

    This function configures the page title, icon, and layout for the
    Streamlit application. It also displays the main title and a brief
    description of the application on the page.
    """
    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="🔍",
        layout="wide"
    )
    st.title("AI Research Assistant")
    st.markdown("""
    This tool helps you research topics using multiple sources:
    - Wikipedia for general knowledge
    - arXiv for scientific papers
    - W3School website information
    """)

def manage_session_state():
    """Manages the Streamlit session state.

    This function initializes the 'agent' and 'messages' in the Streamlit
    session state if they are not already present. The agent is created using
    the `initialize_agent` function, and the messages list is initialized as
    an empty list.
    """
    if 'agent' not in st.session_state:
        with st.spinner('Initializing AI agent...'):
            st.session_state.agent = initialize_agent()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def display_chat_interface():
    """Displays the chat interface and handles user interaction.

    This function is responsible for displaying the chat history and the chat
    input box. When a user enters a query, it is added to the session state,
    and the agent is invoked to get a response. The user's query and the
    agent's response are then displayed in the chat interface.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Ask me anything...")
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Researching..."):
                message_placeholder = st.empty()
                response = st.session_state.agent.invoke({"input": user_query})
                result = response.get("output", "I couldn't find an answer to that question.")
                message_placeholder.markdown(result)

        st.session_state.messages.append({"role": "assistant", "content": result})

def display_sidebar():
    """Displays the sidebar.

    The sidebar contains information about the application and a button to
    clear the conversation history. When the 'Clear Conversation' button is
    clicked, the 'messages' list in the session state is cleared, and the
    page is rerun.
    """
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

        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

def main():
    """The main function to run the AI Research Assistant application.

    This function orchestrates the application by calling the other functions
    in the correct order to set up the page, manage the session state, and
    display the UI components.
    """
    setup_page()
    manage_session_state()
    display_chat_interface()
    display_sidebar()

if __name__ == "__main__":
    main()
