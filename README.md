# GenAI Fact Generator

An AI-powered fact generation system with document storage and retrieval capabilities. Built with FastAPI backend and Streamlit frontend, utilizing OpenAI's GPT models and ChromaDB for document storage.

## 🚀 Features

- Interactive web interface for fact generation
- Document storage and retrieval using ChromaDB
- RAG (Retrieval Augmented Generation) capabilities
- Real-time AI-powered fact creation
- Document management interface
- Error handling and user feedback

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4
- **Vector Database**: ChromaDB
- **Language**: Python 3.12+

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- pip (Python package manager)

## 📁 Project Structure

```
genai-chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── knowledge_base.py    # ChromaDB integration
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
├── data/                    # Created automatically
│   └── chromadb/           # Vector database storage
├── .env                    # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/kaus19/genai-chatbot.git
cd genai-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Running the Application

1. Start the FastAPI backend:
```bash
uvicorn backend.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run frontend/streamlit_app.py
```

3. Access the applications:
- Frontend: http://localhost:8501
- API documentation: http://localhost:8000/docs

## 💡 Usage

1. **Document Management**
   - Upload documents through the web interface
   - View stored documents
   - Add metadata to documents

2. **Fact Generation**
   - Enter a prompt
   - System retrieves relevant context from stored documents
   - Generates facts using both the prompt and context

## 🔧 Development

The application uses:
- ChromaDB for vector storage and retrieval
- FastAPI for the backend API
- Streamlit for the user interface
- OpenAI's GPT models for generation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Kaustubh Maloo (@kaus19)

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- ChromaDB team for the vector database
- FastAPI and Streamlit communities