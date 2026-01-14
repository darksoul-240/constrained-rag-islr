import google.generativeai as genai
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGSystem:
    def __init__(self, embeddings_file, api_key):
        """Initialize RAG system with embeddings and API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Load embeddings
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            self.embeddings_data = json.load(f)
        
        self.embeddings_matrix = np.array([
            item['embedding'] for item in self.embeddings_data
        ])
        
        # Initialize chat model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        print(f"[OK] RAG System initialized with {len(self.embeddings_data)} chunks")
    
    def embed_query(self, query):
        """Convert query to embedding"""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        return np.array(result['embedding'])
    
    def retrieve(self, query, top_k=3):
        """Retrieve top_k most similar chunks"""
        query_embedding = self.embed_query(query)
        
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            self.embeddings_matrix
        )[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'chunk_id': self.embeddings_data[idx]['chunk_id'],
                'text': self.embeddings_data[idx]['text'],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def answer_question(self, question, top_k=3, show_chunks=False):
        """
        Answer a question using RAG:
        1. Retrieve relevant chunks
        2. Build context from chunks
        3. Send to LLM with instruction to use only the context
        """
        # Retrieve relevant chunks
        chunks = self.retrieve(question, top_k=top_k)
        
        # Build context from retrieved chunks
        context = "\n\n---\n\n".join([chunk['text'] for chunk in chunks])
        
        # Create prompt for LLM
        prompt = f"""You are a helpful assistant answering questions about Support Vector Machines from the textbook "An Introduction to Statistical Learning".

CONTEXT FROM THE BOOK:
{context}

QUESTION: {question}

INSTRUCTIONS:
- Answer the question using ONLY the information provided in the context above
- If the context doesn't contain enough information to answer, say so
- Be concise and clear
- Cite specific concepts from the context when relevant

ANSWER:"""
        
        # Get response from LLM
        response = self.model.generate_content(prompt)
        
        # Prepare result
        result = {
            'question': question,
            'answer': response.text,
            'chunks_used': chunks
        }
        
        # Display
        print(f"\nQUESTION: {question}")
        print("-" * 80)
        
        if show_chunks:
            print("\n[RETRIEVED CHUNKS]")
            for i, chunk in enumerate(chunks, 1):
                print(f"\nChunk {i} (similarity: {chunk['similarity']:.3f}):")
                print(chunk['text'][:200] + "...")
            print("\n" + "-" * 80)
        
        print(f"\nANSWER:\n{response.text}")
        print("\n" + "=" * 80)
        
        return result

if __name__ == "__main__":
    print("="*80)
    print("RAG SYSTEM - Support Vector Machines Q&A")
    print("="*80)
    
    api_key = input("\nPaste your Gemini API key: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided.")
        exit(1)
    
    # Initialize RAG system
    rag = RAGSystem(
        embeddings_file="data\embeddings\chapter10_embeddings.json", #replace with respective path for other chapters
        api_key=api_key
    )
    
    # Test questions
    test_questions = [
        "What is a neural nework?",
        "How does backpropagation work?",
        "what are activation functions?",
        "what are best networks for classification/identification?"
        #"What is a support vector?",
        #"What is the maximal margin hyperplane?",
        #"Explain the optimization problem for support vector classifier"
        "What is a convolutional neural network?"

    ]
    
    print("\n" + "="*80)
    print("RUNNING TEST QUESTIONS")
    print("="*80)
    
    for question in test_questions:
        rag.answer_question(question, show_chunks=True)
        input("\nPress Enter to continue...")
    
    # Interactive mode
    print("\n" + "="*80)
    print("INTERACTIVE MODE")
    print("Commands: 'chunks' to show retrieved chunks, 'quit' to exit")
    print("="*80)
    
    show_chunks = False
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if question.lower() == 'chunks':
            show_chunks = not show_chunks
            print(f"[Chunk display: {'ON' if show_chunks else 'OFF'}]")
            continue
        
        if not question:
            continue
        
        try:
            rag.answer_question(question, show_chunks=show_chunks)
        except Exception as e:
            print(f"Error: {e}")