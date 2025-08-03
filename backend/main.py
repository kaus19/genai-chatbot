from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from .knowledge_base import KnowledgeBase
from .knowledge_base import Message
from typing import List
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize knowledge base
kb = KnowledgeBase()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Define request model
class FactRequest(BaseModel):
    prompt: str

# Define response model
class FactResponse(BaseModel):
    fact: str

class DocumentUpload(BaseModel):
    content: str
    metadata: dict = {}

@app.get("/documents")
async def get_documents():
    try:
        docs = kb.get_all_documents()
        stats = kb.peek_collection()
        return {
            "collection_stats": stats,
            "documents": docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(document: DocumentUpload):
    try:
        # Add the document
        kb.add_documents([document.content], [document.metadata])
        
        # Verify addition
        all_docs = kb.get_all_documents()
        logger.info(f"Total documents after addition: {len(all_docs)}")
        
        return {
            "message": "Document uploaded successfully",
            "current_count": len(all_docs)
        }
    except Exception as e:
        logger.error(f"Error in upload_document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate-fact", response_model=FactResponse)
async def generate_fact(request: FactRequest):
    try:
         # Retrieve relevant context from knowledge base
        context = kb.query(request.prompt)

         # Construct prompt with context
        context_text = "\n".join([doc['text'] for doc in context])
        enhanced_prompt = f"""Context information:
            {context_text}

            Using the context above if relevant, please tell me a fact on this prompt:
            {request.prompt}"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fact teller that uses provided context when relevant."},
                {"role": "user", "content": enhanced_prompt}
            ]
        )
        return FactResponse(fact=response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


class ChatMessage(BaseModel):
    content: str
    role: str

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        # Add user message to history
        kb.add_message(Message(
            content=message.content,
            role="user"
        ))
        
        # Get context from knowledge base
        context = kb.get_context_for_query(message.content)
        
        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer questions."},
                {"role": "user", "content": f"Context:\n{context}\n\nUser Question: {message.content}"}
            ]
        )
        
        # Extract assistant's response
        assistant_response = response.choices[0].message.content
        
        # Add assistant's response to history
        kb.add_message(Message(
            content=assistant_response,
            role="assistant"
        ))
        
        return {
            "response": assistant_response,
            "chat_history": kb.get_chat_history()
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))