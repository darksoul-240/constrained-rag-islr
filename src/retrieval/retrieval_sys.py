import google.generativeai as genai
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGRetriever:
    def __init__(self, embeddings_file, api_key):
        """Initialize retriever with embeddings and API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Load embeddings
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            self.embeddings_data = json.load(f)
        
        # Extract embeddings as numpy array for fast similarity search
        self.embeddings_matrix = np.array([
            item['embedding'] for item in self.embeddings_data
        ])
        
        print(f"[OK] Loaded {len(self.embeddings_data)} embeddings")
    
    def embed_query(self, query):
        """Convert query to embedding"""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        return np.array(result['embedding'])
    
    def retrieve(self, query, top_k=3):
        """
        Retrieve top_k most similar chunks to the query.
        
        Returns list of dicts with chunk_id, text, and similarity score.
        """
        # Embed the query
        query_embedding = self.embed_query(query)
        
        # Calculate cosine similarity between query and all chunks
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            self.embeddings_matrix
        )[0]
        
        # Get top_k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results
        results = []
        for idx in top_indices:
            results.append({
                'chunk_id': self.embeddings_data[idx]['chunk_id'],
                'text': self.embeddings_data[idx]['text'],
                'similarity': float(similarities[idx])
            })
        
        return results

def test_retrieval(retriever):
    """Test the retrieval system with sample questions"""
    
    test_questions = [
        "What is a neural nework?",
        "How does backpropagation work?",
        "what are activation functions?",
        "what are best classifier algorithms?"
        #"What is a support vector?",
        #"How does the maximal margin hyperplane work?",
        #"What is the role of slack variables in SVM?"
    ]
    
    print("\n" + "="*60)
    print("TESTING RETRIEVAL SYSTEM")
    print("="*60)
    
    for question in test_questions:
        print(f"\nQUESTION: {question}")
        print("-" * 60)
        
        results = retriever.retrieve(question, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n[CHUNK {i}] (similarity: {result['similarity']:.3f})")
            print(result['text'][:300] + "...")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    print("Setting up RAG Retriever...")
    
    api_key = input("Paste your Gemini API key: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided.")
        exit(1)
    
    # Initialize retriever
    retriever = RAGRetriever(
        embeddings_file="data\embeddings\chapter10_embeddings.json", #replace with respective path for other chapters
        api_key=api_key
    )
    
    # Run tests
    test_retrieval(retriever)
    
    # Interactive mode
    print("\n" + "="*60)
    print("INTERACTIVE MODE - Ask your own questions!")
    print("Type 'quit' to exit")
    print("="*60)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        results = retriever.retrieve(question, top_k=3)
        
        print("\n--- RETRIEVED CHUNKS ---")
        for i, result in enumerate(results, 1):
            print(f"\n[CHUNK {i}] (similarity: {result['similarity']:.3f})")
            print(result['text'][:400] + "...")