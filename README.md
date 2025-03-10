# AI Research Assistant 🔍

## Overview

The **AI Research Assistant** is a Streamlit-based web application designed to help users research topics using multiple sources, including Wikipedia, arXiv, and a custom knowledge base. The application leverages LangChain for agent orchestration, Ollama for local LLM inference, and integrates with various APIs to provide comprehensive research capabilities.

## Features

- **Wikipedia Integration**: Fetch general knowledge information from Wikipedia.
- **arXiv Integration**: Search for scientific papers and research articles.
- **Custom Knowledge Base**: Retrieve information from a custom knowledge base (e.g., HiAnime website).
- **Chat Interface**: Interactive chat interface powered by Streamlit.
- **Local LLM Inference**: Utilizes Ollama for local language model inference.

## Technologies Used

- **LangChain**: For agent orchestration and tool integration.
- **Ollama**: For local LLM inference.
- **Streamlit**: For building the web application interface.
- **Wikipedia API**: For fetching general knowledge.
- **arXiv API**: For accessing scientific papers.
- **FAISS**: For vector storage and retrieval.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/naman-kumar1212/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On MacOs, use `source venv/bin/activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your `LANGCHAIN_API_KEY` and any other required API keys:
     ```plaintext
     LANGCHAIN_API_KEY=your_langchain_api_key
     ```

5. **Install Ollama Models**:
   - Run the following commands to download and set up the required Ollama models:
     ```bash
     ollama run llama3.2
     ollama pull nomic-embed-text
     ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

7. **Access the application**:
   - Open your browser and navigate to `http://localhost:8501`.

## Usage

1. **Ask Questions**: Use the chat input to ask questions about any topic.
2. **View Responses**: The assistant will fetch information from Wikipedia, arXiv, and the custom knowledge base.
3. **Clear Conversation**: Use the "Clear Conversation" button in the sidebar to reset the chat history.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://www.langchain.com/) for agent orchestration.
- [Ollama](https://ollama.ai/) for local LLM inference.
- [Streamlit](https://streamlit.io/) for the web interface.
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) and [arXiv API](https://arxiv.org/help/api) for data sources.
