---
id: knowledge-base-manifest
title: Abhishek Yadav - Knowledge Base Index & RAG Manifest
entity: Abhishek Yadav
category: meta
tags:
  - knowledge-base
  - rag
  - index
  - manifest
summary: Index, structural schema, and ingestion guide for Abhishek Yadav's standalone knowledge base, optimized for vector database indexing and RAG retrieval pipelines.
---

# Abhishek Yadav - Knowledge Base Index

This directory contains a structured, modular knowledge base extracted directly and factually from Abhishek Yadav's official resume. Every document is optimized for Retrieval-Augmented Generation (RAG) pipelines, semantic vector search, and LLM context injection.

---

## Directory Structure

```text
knowledge/
├── README.md                 # Knowledge base manifest & RAG indexing guide
├── about.md                  # Personal profile, location, contact, and high-level summary
├── education.md              # University, B.Tech degree, CGPA, and core coursework
├── skills.md                 # Categorized technical competencies, tools, and languages
├── experience.md             # Hands-on experience, responsibilities, and achievements
├── projects.md               # Projects directory overview and comparative matrix
├── projects/
│   ├── money-ledger.md       # Money Ledger: offline-first finance webapp (Next.js, Dexie.js, Firebase)
│   ├── arkface.md            # ArkFace: real-time face recognition (.exe, Python, OpenCV, MediaPipe)
│   └── quizai.md             # QuizAI: adaptive AI quiz platform (Next.js, Groq API, MongoDB)
├── achievements.md           # Hackathons (HackerRank Orchestrate #766/1,983), DSA problem solving
├── certifications.md         # Professional workshops & certifications (GFG, HCL GUVI, Azisly)
├── profiles.md               # GitHub (@AKabhishek9), LinkedIn, LeetCode, and portfolio links
└── resume.md                 # Complete, monolithic resume transcript in markdown format
```

---

## RAG Optimization Characteristics
Each document in this knowledge base has been intentionally engineered with:
1. **Explicit Entity Grounding**: "Abhishek Yadav" is explicitly declared throughout headings and body copy to ensure chunks retain context after vector splitting without pronoun ambiguity.
2. **Standard YAML Frontmatter**: Every file includes structured metadata (`id`, `title`, `entity`, `category`, `tags`, `keywords`, `summary`) for hybrid search (dense embeddings + metadata filtering).
3. **Semantic Hierarchy**: Clear, distinct Markdown headers (`#`, `##`, `###`) and markdown tables provide natural chunk boundaries for recursive character splitters.
4. **Target RAG Retrieval Queries**: Explicit query prompts at the conclusion of each document optimize semantic similarity against anticipated user questions.
5. **Strict Factual Accuracy**: Contains only verified facts extracted from Abhishek Yadav's official resume without hallucinated additions.
