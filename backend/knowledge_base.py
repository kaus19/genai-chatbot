import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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