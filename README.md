# AI Story Generator

An interactive web application that generates stories using OpenAI's GPT-4 model. Built with FastAPI backend and Streamlit frontend.

## 🚀 Features

- Interactive web interface for story generation
- Real-time AI-powered story creation
- Error handling and user feedback
- Simple and intuitive UI

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4
- **Language**: Python 3.12+

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- pip (Python package manager)

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

3. Create a `.env` file in the project root:
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

3. Open your browser and navigate to:
- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## 📁 Project Structure

```
genai-chatbot/
├── backend/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── .env
├── requirements.txt
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Kaustubh Maloo - Initial work

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- FastAPI and Streamlit communities