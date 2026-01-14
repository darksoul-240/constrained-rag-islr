import pdfplumber
import re

def clean_text(text):
    """
    Clean extracted text from common PDF artifacts.
    """
    # Fix common spacing issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
    text = re.sub(r'([a-z])(\d)', r'\1 \2', text)     # Add space between letter and number
    text = re.sub(r'(\d)([a-z])', r'\1 \2', text)     # Add space between number and letter
    
    # Fix multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Fix line breaks (keep paragraph breaks, remove mid-sentence breaks)
    text = re.sub(r'(?<![.!?])\n(?=[a-z])', ' ', text)  # Join mid-sentence breaks
    text = re.sub(r'\n+', '\n\n', text)  # Normalize paragraph breaks
    
    return text.strip()

def extract_chapter_10_clean(pdf_path):
    """
    Extract Chapter 10 using pdfplumber for better text extraction.
    """
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        # Pages 406-475 (0-indexed: 405-474)
        start_page = 405
        end_page = 474
        
        for page_num in range(start_page, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    
    # Clean the extracted text
    text = clean_text(text)
    
    return text

if __name__ == "__main__":
    pdf_path = r"C:\Users\Ibrahim\Documents\Career\Projects\RAG_Project\ISLR.pdf"
    
    print("Extracting Chapter 10 with pdfplumber...")
    chapter_text = extract_chapter_10_clean(pdf_path)
    
    # Save to file
    with open("chapter10_clean.txt", "w", encoding="utf-8") as f:
        f.write(chapter_text)
    
    # Basic stats
    print(f"[OK] Extracted {len(chapter_text)} characters")
    print(f"[OK] Approximately {len(chapter_text.split())} words")
    print(f"[OK] Saved to chapter9_clean.txt")
    
    # Show a sample (safe for console)
    print("\n--- Sample (first 300 chars) ---")
    try:
        print(chapter_text[:300])
    except:
        print("[Console encoding issue - but file is saved correctly]")