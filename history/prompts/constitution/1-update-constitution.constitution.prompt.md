---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-31
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Claude Code
command: sp.constitution
labels: [constitution, spec-driven-development, rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
---

## Prompt

```
Project: Unified AI-Generated Book with Embedded RAG Chatbot

Core Principles:

Spec-Driven Development: The entire book must be written using Claude Code with Spec-Kit Plus as the primary framework.

Full Integration: The published book must contain a fully functional RAG chatbot embedded within it.

Content Integrity: The chatbot must answer questions based only on the book's actual content.

User-Centric Selection: The chatbot must be capable of answering questions based on user-selected text from the book.

Key Technical Standards:

Book Stack: Docusaurus for generation and GitHub Pages for deployment.

RAG Stack:

SDK/API: OpenAI Agents/ChatKit SDKs with FastAPI backend.

Database: Neon Serverless Postgres for chat history/metadata.

Vector Store: Qdrant Cloud Free Tier for book content embeddings.

Chatbot Functionality:

General Q&A about the entire book's content.

Context-specific Q&A based on user-highlighted or selected text passages.

Answers must be strictly grounded in the provided book text; no external knowledge unless specified in the book.

Code Quality: All code (book build, RAG pipeline, API) must be production-ready, documented, and hosted per specifications.

Constraints:

Primary Tools: Claude Code and Spec-Kit Plus are mandatory for the book authoring phase.

Deployment: The final, functional book with its embedded chatbot must be publicly accessible via GitHub Pages.

Architecture: The system must be a cohesive unit; the chatbot is not a separate application but a feature of the book.

Success Criteria:

Book Published: A complete, well-formatted book is live on GitHub Pages.

Chatbot Operational: The embedded RAG chatbot is active and responsive on the live book site.

Accuracy Test: The chatbot correctly answers questions using the book as its sole knowledge source.

Selection Feature: The "answer based on selected text" feature works reliably and accurately.

Repo Integrity: The GitHub repository contains all source code, build scripts, and clear setup instructions for full reproducibility.
```

## Response snapshot

Updated the constitution file with the new project principles for the Unified AI-Generated Book with Embedded RAG Chatbot project. The constitution now includes:

1. Core Principles:
   - Spec-Driven Development
   - Full Integration
   - Content Integrity
   - User-Centric Selection
   - Production-Ready Code Quality
   - Technology Stack Compliance

2. Technical Standards:
   - Book Stack (Docusaurus, GitHub Pages)
   - RAG Stack (OpenAI Agents/ChatKit, Neon Postgres, Qdrant)
   - Chatbot Functionality Requirements

3. Development Workflow:
   - Primary Tools Mandate (Claude Code, Spec-Kit Plus)
   - Quality Assurance Process

4. Governance section with versioning and amendment procedures

Also updated the plan template to include constitution check gates that align with the new principles.

## Outcome

- ✅ Impact: Created new constitution for the AI-generated book project with RAG chatbot
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md and .specify/templates/plan-template.md
- 🔁 Next prompts: N/A
- 🧠 Reflection: The constitution now properly reflects the project requirements and will guide future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A