import json

def chunk_text(text, chunk_size=550, overlap=150):
    """
    Split text into overlapping chunks.
    
    Strategy:
    - Split on paragraph boundaries (double newlines)
    - Build chunks up to chunk_size
    - Add overlap by including last 'overlap' chars from previous chunk
    """

    paragraphs=text.split("\n\n")
    paragraphs=[p.strip() for p in paragraphs if p.strip()]

    chunks=[]
    current_chunk=""

    for para in paragraphs:
        if len(current_chunk)+len(para)>chunk_size and current_chunk:
            chunks.append(current_chunk.strip())

            current_chunk=current_chunk[-overlap:] if len(current_chunk)>overlap else current_chunk

        current_chunk+=para+"\n\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def save_chunks(chunks,output_file):
    """
    Save chunks with metadata to JSON file.

    """
    chunk_data=[]
    for i,chunk in enumerate(chunks):
        chunk_data.append({
            "id":f"chunk_{i}",
            "text":chunk,
            "char_count":len(chunk),
            "word_count":len(chunk.split())
        })
    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(chunk_data,f,indent=2,ensure_ascii=False)
    return chunk_data

if __name__=="__main__":
    # Load the clean text
    with open("chapter10_clean.txt","r",encoding="utf-8") as f:
        text=f.read()
    
    print("Chunking Chapter 10...")
    chunks=chunk_text(text,chunk_size=550,overlap=150)
    
    print(f"Generated {len(chunks)} chunks.")
    
    # Save chunks to file
    chunk_data=save_chunks(chunks,"chunks/chapter10_chunks.json")
    
    print("Chunks saved to chunks/chapter10_chunks.json")