# GenAI Chatbot

An AI-powered chatbot with fact generation and document storage capabilities. Built with FastAPI backend and Streamlit frontend, utilizing OpenAI's GPT-4 and ChromaDB for knowledge management.

## 🚀 Features

### 💬 Interactive Chat
- Real-time chat interface with AI assistant
- Context-aware responses using RAG (Retrieval Augmented Generation)
- Persistent chat history using ChromaDB
- Message threading and conversation memory

### 📚 Document Management
- Document storage and retrieval using ChromaDB
- Metadata support for documents
- Document search and querying

### 🎯 Fact Generation
- AI-powered fact generation
- Context-enhanced responses
- Document-based knowledge integration

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
│   ├── main.py              # FastAPI endpoints including chat
│   └── knowledge_base.py    # ChromaDB integration & chat history
├── frontend/
│   └── streamlit_app.py     # Streamlit UI with chat interface
├── data/                    # Created automatically
│   └── chromadb/           # Vector database & chat storage
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
- Frontend UI: http://localhost:8501
- API documentation: http://localhost:8000/docs

## 💡 Usage

### Chat Interface
1. Navigate to the "Chat" tab
2. Type your message in the input field
3. The AI will respond using:
   - Relevant context from uploaded documents
   - Previous conversation history
   - General knowledge from GPT-4

### Document Management
1. Go to the "Documents" tab
2. Upload documents with optional metadata
3. View and manage stored documents

### Fact Generation
1. Select the "Fact Generator" tab
2. Enter a topic or question
3. Receive AI-generated facts based on stored knowledge

## 🔧 Development

The application uses:
- ChromaDB for vector storage and chat history
- FastAPI for RESTful API endpoints
- Streamlit for interactive UI
- OpenAI's GPT-4 for intelligent responses

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.