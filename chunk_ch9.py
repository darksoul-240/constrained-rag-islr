import json

def chunk_text(text, chunk_size=900, overlap=200):
    """
    Split text into overlapping chunks.
    
    Strategy:
    - Split on paragraph boundaries (double newlines)
    - Build chunks up to chunk_size
    - Add overlap by including last 'overlap' chars from previous chunk
    """
    # Split into paragraphs
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # If adding this paragraph exceeds chunk_size, save current chunk
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap from previous
            current_chunk = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
        
        # Add paragraph to current chunk
        current_chunk += para + "\n\n"
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def save_chunks(chunks, output_file):
    """
    Save chunks with metadata to JSON file.
    """
    chunk_data = []
    for i, chunk in enumerate(chunks):
        chunk_data.append({
            "id": f"chunk_{i}",
            "text": chunk,
            "char_count": len(chunk),
            "word_count": len(chunk.split())
        })
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2, ensure_ascii=False)
    
    return chunk_data

if __name__ == "__main__":
    # Load the clean text
    with open("chapter9_clean.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    print("Chunking Chapter 9...")
    chunks = chunk_text(text, chunk_size=900, overlap=200)
    
    print(f"[OK] Created {len(chunks)} chunks")
    
    # Save chunks
    chunk_data = save_chunks(chunks, "chunks/chapter9_chunks.json")
    
    # Stats
    avg_size = sum(c['char_count'] for c in chunk_data) / len(chunk_data)
    print(f"[OK] Average chunk size: {avg_size:.0f} characters")
    print(f"[OK] Saved to chunks/chapter9_chunks.json")
    
    # Show first chunk as sample
    print("\n--- FIRST CHUNK (preview) ---")
    print(chunk_data[0]['text'][:300] + "...")
    
    # Show chunk size distribution
    print("\n--- CHUNK SIZE DISTRIBUTION ---")
    sizes = [c['char_count'] for c in chunk_data]
    print(f"Min: {min(sizes)} | Max: {max(sizes)} | Avg: {avg_size:.0f}")