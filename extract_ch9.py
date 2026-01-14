import PyPDF2

def extract_chapter_9(pdf_path):
    """
    Extract Chapter 9 (Support Vector Machines) from ISLR.
    Chapter 9 typically starts around page 337 and ends around page 368.
    Adjust page numbers if your PDF version differs.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # ISLR Chapter 9 page range (0-indexed in PyPDF2)
        # Adjust these if your PDF has different numbering
        start_page = 374  # Page 337 in the book
        end_page = 405    # Page 368 in the book
        
        text = ""
        for page_num in range(start_page, min(end_page, len(reader.pages))):
            page = reader.pages[page_num]
            text += page.extract_text()
        
        return text

if __name__ == "__main__":
    pdf_path = r"C:\\Users\\Ibrahim\\Documents\\Career\\Projects\\RAG_Project\\ISLR.pdf"
    
    print("Extracting Chapter 9...")
    chapter_text = extract_chapter_9(pdf_path)
    
    # Save to file
    with open("chapter9_raw.txt", "w", encoding="utf-8") as f:
        f.write(chapter_text)
    
    # Basic stats
    print(f" Extracted {len(chapter_text)} characters")
    print(f" Approximately {len(chapter_text.split())} words")
    print(" Saved to chapter9_raw.txt")
    print("\nFirst 500 characters:")
    print(chapter_text[:500])