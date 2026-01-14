📘 Constrained Retrieval-Augmented Generation (RAG) System
Overview

This project implements a constrained Retrieval-Augmented Generation (RAG) system that answers user queries strictly using retrieved context from a fixed knowledge source. The system explicitly identifies and rejects queries that lack sufficient contextual grounding, preventing hallucinated responses.

The knowledge source is selected chapters from An Introduction to Statistical Learning (ISLR), enabling controlled evaluation of retrieval quality and answer correctness.

Data Source

Book: An Introduction to Statistical Learning

Chapters used:

Chapter 9 — Support Vector Machines (SVM)

Chapter 10 — Deep Learning

The chapters were intentionally chosen to include both:

Familiar content (SVM) for validation

Unfamiliar, concept-dense content (Deep Learning) to observe retrieval failure modes

System Pipeline

1. PDF Parsing
Text was extracted from the ISLR PDF using:

PyPDF2 (initial attempt)

pdfplumber (final choice due to superior layout and spacing preservation)

Parsing limitations such as broken spacing and extraneous line breaks were identified and documented.

2. Chunking Strategy
Chunks were created using chapter-specific strategies based on content density and conceptual continuity:

Chapter 9 (SVM):

Larger chunk size

Moderate overlap

Preserves mathematical and conceptual flow

Chapter 10 (Deep Learning):

Smaller chunk size

Higher overlap

Mitigates rapid abstraction shifts and dependency chains

Chunks were stored as JSON objects with unique chunk identifiers.

3. Embedding

Embeddings were generated using the Gemini API

Each chunk was embedded into a 768-dimensional vector

Chapter 9 and Chapter 10 were indexed separately to isolate retrieval behavior

4. Retrieval

User queries are embedded using the same embedding model

Cosine similarity is used to retrieve the top-k most relevant chunks

Retrieval quality is explicitly inspected before generation

5. Generation (RAG)

Retrieved chunks are injected as context into the LLM

The model answers only if sufficient contextual grounding exists

Ambiguous or unrelated queries result in explicit “insufficient context” responses

Observations & Learnings

PDF parsing introduces non-trivial noise that affects downstream chunking

Chunk size and overlap must be data-dependent, not fixed

Semantic retrieval fails silently without proper overlap in dense material

Query quality directly controls retrieval success in constrained systems

Separating familiar and unfamiliar content improves debugging and evaluation