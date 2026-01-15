
---

# 📘 Constrained Retrieval-Augmented Generation (RAG) System

## 🎯 Overview

This project implements a **constrained Retrieval-Augmented Generation (RAG) system** that answers user queries strictly using retrieved context from a fixed knowledge source. The system explicitly identifies and rejects queries that lack sufficient contextual grounding, preventing hallucinated responses.

The knowledge source is selected chapters from **An Introduction to Statistical Learning (ISLR)**, enabling controlled evaluation of retrieval quality and answer correctness.

---

## 📚 Data Source

**Book:** *An Introduction to Statistical Learning*

**Chapters used:**
- **Chapter 9** — Support Vector Machines (SVM)
- **Chapter 10** — Deep Learning

The chapters were intentionally chosen to include both:
- ✅ **Familiar content** (SVM) for validation
- ⚠️ **Unfamiliar, concept-dense content** (Deep Learning) to observe retrieval failure modes

---

## 🔧 System Pipeline

### 1️⃣ PDF Parsing
Text was extracted from the ISLR PDF using:
- `PyPDF2` (initial attempt)
- `pdfplumber` ✅ (final choice due to superior layout and spacing preservation)

**Note:** Parsing limitations such as broken spacing and extraneous line breaks were identified and documented.

### 2️⃣ Chunking Strategy
Chunks were created using **chapter-specific strategies** based on content density and conceptual continuity:

| Chapter | Chunk Size | Overlap | Rationale |
|---------|-----------|---------|-----------|
| **Chapter 9 (SVM)** | Larger | Moderate | Preserves mathematical and conceptual flow |
| **Chapter 10 (Deep Learning)** | Smaller | Higher | Mitigates rapid abstraction shifts and dependency chains |

Chunks were stored as JSON objects with unique chunk identifiers.

### 3️⃣ Embedding
- Embeddings were generated using the **Gemini API**
- Each chunk was embedded into a **768-dimensional vector space**
- Chapter 9 and Chapter 10 were indexed separately to isolate retrieval behavior
- **Total chunks:** 578 (117 for SVM + 461 for Deep Learning)

### 4️⃣ Retrieval
- User queries are embedded using the same embedding model
- **Cosine similarity** is used to retrieve the top-k most relevant chunks
- Retrieval quality is explicitly inspected before generation

### 5️⃣ Generation (RAG)
- Retrieved chunks are injected as context into the LLM
- The model answers **only if sufficient contextual grounding exists**
- Ambiguous or unrelated queries result in explicit **"insufficient context"** responses

---

## 💡 Key Observations & Learnings

| Insight | Description |
|---------|-------------|
|  **PDF parsing is non-trivial** | Introduces noise (spacing issues, line breaks) that affects downstream chunking |
|  **Chunking must be data-dependent** | Chunk size and overlap cannot be fixed—they must adapt to content structure |
|  **Overlap prevents retrieval failures** | Dense material requires higher overlap to maintain context continuity |
|  **Query quality controls retrieval** | Specific queries (0.81 similarity) vastly outperform vague queries (0.58 similarity) |
|  **Familiarity aids debugging** | Separating known and unknown content improves evaluation and failure analysis |

---

##  How to Run

```bash
# 1. Extract text from PDF
python extract_chapter9_clean.py
python extract_chapter10_clean.py

# 2. Chunk the extracted text
python chunk_chapter9.py
python chunk_chapter10.py

# 3. Generate embeddings (requires Gemini API key)
python generate_embeddings.py

# 4. Run the RAG system
python rag_system.py
```

---

##  Example Results

| Question | Similarity Score | Result |
|----------|-----------------|--------|
| "What is a hyperplane?" | 0.81 | ✅ Perfect retrieval and answer |
| "What is a CNN?" | 0.72 | ✅ Accurate explanation with context |
| "What are best classifiers?" | 0.58 | ⚠️ Insufficient context, system states limitations |

---

##  Tech Stack

- **Python** — Core language
- **Gemini API** — Embeddings + LLM generation
- **pdfplumber** — PDF text extraction
- **scikit-learn** — Cosine similarity computation
- **NumPy** — Vector operations

---

##  Known Limitations

- PDF extraction still contains spacing artifacts (visible in retrieval outputs)
- Vague or abstract queries yield low-confidence retrievals
- System cannot currently compare or synthesize across chapters

---

## 🤝 Feedback

Feedback and suggestions are always welcome! Feel free to open an issue or reach out.

---

**Would you like any adjustments to the style or structure?**
