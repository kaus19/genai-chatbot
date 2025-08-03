import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message:
    def __init__(self, content: str, role: str, timestamp: Optional[datetime] = None):
        self.content = content
        self.role = role  # "user" or "assistant"
        self.timestamp = timestamp or datetime.now()

class KnowledgeBase:
    def __init__(self):
        # Ensure data directory exists
        os.makedirs("./data/chromadb", exist_ok=True)
        
        # Initialize ChromaDB client with new configuration
        self.client = chromadb.PersistentClient(
            path="./data/chromadb"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="fact_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

         # Create a separate collection for chat history
        self.chat_collection = self.client.get_or_create_collection(
            name="chat_history",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, texts: List[str], metadata: List[Dict] = None):
        """Add documents to the knowledge base"""
        try:
            if metadata is None:
                metadata = [{}] * len(texts)
            
            # Get current count to offset IDs
            current_count = self.collection.count()
            
            # Generate unique IDs for documents
            ids = [f"doc_{current_count + i}" for i in range(len(texts))]
            
            logger.info(f"Adding {len(texts)} documents to collection")
            logger.info(f"Current collection count: {self.collection.count()}")
            
            # Add documents to collection
            self.collection.add(
                documents=texts,
                metadatas=metadata,
                ids=ids
            )
            
            new_count = self.collection.count()
            logger.info(f"New collection count: {new_count}")
            
            # Verify addition
            if new_count != current_count + len(texts):
                logger.warning(f"Expected {current_count + len(texts)} documents, but got {new_count}")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """Query the knowledge base"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return [{
            'text': doc,
            'metadata': meta
        } for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
    
    def get_all_documents(self) -> List[Dict]:
        """Retrieve all documents from the knowledge base"""
        try:
            # Get the count of documents
            collection_count = self.collection.count()
            
            if collection_count == 0:
                return []
            
            # Query all documents
            results = self.collection.get(
                limit=collection_count
            )
            
            return [{
                'id': id,
                'text': doc,
                'metadata': meta
            } for id, doc, meta in zip(
                results['ids'], 
                results['documents'], 
                results['metadatas']
            )]
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def peek_collection(self) -> Dict:
        """Get collection statistics"""
        return {
            'name': self.collection.name,
            'count': self.collection.count(),
            'metadata': self.collection.metadata
        }
    
    def add_message(self, message: Message):
        """Add a message to chat history"""
        try:
            # Get current count for ID generation
            current_count = self.chat_collection.count()
            
            # Create message document
            self.chat_collection.add(
                documents=[message.content],
                metadatas=[{
                    "role": message.role,
                    "timestamp": message.timestamp.isoformat()
                }],
                ids=[f"msg_{current_count}"]
            )
            
            logger.info(f"Added message to chat history: {message.role}")
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            raise

    def get_chat_history(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent chat history"""
        try:
            # Get total message count
            total_messages = self.chat_collection.count()
            if total_messages == 0:
                return []
            
            # Query recent messages
            results = self.chat_collection.get(
                limit=min(limit, total_messages)
            )

            # Convert to list of messages
            messages = []
            for i in range(len(results['ids'])):
                messages.append({
                    'id': results['ids'][i],
                    'content': results['documents'][i],
                    'role': results['metadatas'][i]['role'],
                    'timestamp': datetime.fromisoformat(results['metadatas'][i]['timestamp'])
                })
            
            # Sort by timestamp
            return sorted(messages, key=lambda x: x['timestamp'])
        except Exception as e:
            logger.error(f"Error retrieving chat history: {e}")
            return []
        
    def get_context_for_query(self, query: str, n_results: int = 3) -> str:
        """Get relevant context from both documents and chat history"""
        try:
            # Query documents
            doc_results = self.query(query, n_results=n_results)
            
            # Query chat history
            chat_results = self.chat_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Combine context
            context = []
            
            # Add relevant documents
            for doc in doc_results:
                context.append(f"Document: {doc['text']}")
            
            # Add relevant chat history
            for msg, meta in zip(chat_results['documents'][0], chat_results['metadatas'][0]):
                context.append(f"{meta['role'].capitalize()}: {msg}")
            
            return "\n".join(context)
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return ""