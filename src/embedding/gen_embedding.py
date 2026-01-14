import google.generativeai as genai
import json
import time
import numpy as np

def setup_gemini(api_key):
    """Configure Gemini API"""
    genai.configure(api_key=api_key)

def generate_embeddings(chunks, api_key):
    """
    Generate embeddings for all chunks using Gemini.
    
    Returns list of dicts with chunk_id, text, and embedding.
    """
    setup_gemini(api_key)
    
    embeddings_data = []
    
    for i, chunk in enumerate(chunks):
        try:
            # Generate embedding using Gemini's embedding model
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=chunk['text'],
                task_type="retrieval_document"
            )
            
            embedding = result['embedding']
            
            embeddings_data.append({
                'chunk_id': chunk['id'],
                'text': chunk['text'],
                'embedding': embedding
            })
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(chunks)} chunks...")
            
            # Rate limiting - be nice to the API
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error on chunk {i}: {e}")
            continue
    
    return embeddings_data

def save_embeddings(embeddings_data, output_file):
    """Save embeddings to file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, ensure_ascii=False)

if __name__ == "__main__":
    # Load chunks
    with open("data\chunks\chapter10_chunks.json", "r", encoding="utf-8") as f:   #replace with respective path for other chapters
        chunks = json.load(f)   
    print(f"Loaded {len(chunks)} chunks")
    print("\nIMPORTANT: You need to paste your Gemini API key now.")
    print("(It won't be saved anywhere, just used for this session)")
    
    api_key = input("\nPaste your Gemini API key here: ").strip()
    
    if not api_key:
        print("ERROR: No API key provided. Exiting.")
        exit(1)
    
    print("\nGenerating embeddings...")
    
    embeddings_data = generate_embeddings(chunks, api_key)
    
    # Save embeddings
    output_file = "data\embeddings\chapter10_embeddings.json"
    save_embeddings(embeddings_data, output_file)
    
    print(f"\n[OK] Generated {len(embeddings_data)} embeddings")
    print(f"[OK] Saved to {output_file}")
    print(f"[OK] Each embedding has {len(embeddings_data[0]['embedding'])} dimensions")