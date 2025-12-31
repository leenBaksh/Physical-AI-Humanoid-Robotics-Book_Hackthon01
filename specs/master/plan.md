# Implementation Plan: Physical AI & Humanoid Robotics Book with RAG Chatbot

**Branch**: `master` | **Date**: 2025-12-31 | **Spec**: [specs/master/spec.md](spec.md)
**Input**: Feature specification from `/specs/master/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This project implements a comprehensive technical book on Physical AI and Humanoid Robotics with embedded RAG (Retrieval Augmented Generation) chatbot functionality. The system includes a Docusaurus-based book with two modules (ROS 2 fundamentals and Gazebo/Unity digital twin concepts), a FastAPI backend for the RAG pipeline using Neon Postgres and Qdrant vector store, and an integrated ChatKit widget for content-based Q&A. The book is deployed to GitHub Pages while the RAG API is hosted on a public platform.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend), Node.js (Docusaurus)
**Primary Dependencies**: Docusaurus (book generation), FastAPI (backend API), Neon Postgres (metadata), Qdrant (vector store), OpenAI/ChatKit (chatbot SDK)
**Storage**: Neon Serverless Postgres for chat history/metadata, Qdrant Cloud Free Tier for book content embeddings
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web browser (GitHub Pages deployment) with FastAPI backend
**Project Type**: Web/documentation with embedded chatbot functionality - determines source structure
**Performance Goals**: <2 seconds API response time for 90% of requests, <3 seconds page load time for 90% of users
**Constraints**: <200ms p95 response time for 90% of API requests, GitHub Pages hosting limitations, Free tier service constraints
**Scale/Scope**: Supports 1000+ concurrent users, 100+ book pages, 500+ content chunks in vector database

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development Compliance

- [x] Feature specification exists in `/specs/master/spec.md`
- [x] Implementation approach aligns with Spec-Driven Development methodology
- [x] Proper specifications, plans, and task breakdowns will be followed

### Full Integration Verification

- [x] Architecture supports embedded RAG chatbot functionality
- [x] Integration approach maintains cohesive user experience
- [x] Chatbot is designed as integrated component, not separate application

### Content Integrity Assurance

- [x] System design ensures chatbot answers only from book content
- [x] Content grounding mechanisms are planned
- [x] No external knowledge injection pathways exist

### User-Centric Selection Support

- [x] Architecture supports user text selection functionality
- [x] Context-specific Q&A capabilities are planned
- [x] Highlighted/selected text processing is addressed

### Production-Ready Code Standards

- [x] Code quality plans meet production requirements
- [x] Documentation strategy is included
- [x] Security and performance considerations are addressed

### Technology Stack Compliance

- [x] Architecture aligns with specified tech stack (Docusaurus, OpenAI Agents/ChatKit, Neon Postgres, Qdrant)
- [x] Dependencies and frameworks match constitution requirements

## Project Structure

### Documentation (this feature)

```text
specs/master/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application with separate frontend (Docusaurus) and backend (FastAPI)
docs/
├── module1/             # Module 1 content (ROS 2 fundamentals)
├── module2/             # Module 2 content (Gazebo/Unity digital twin)
├── index.md             # Book homepage
├── sidebars.js          # Navigation configuration
└── docusaurus.config.js # Site configuration

backend/
├── src/
│   ├── models/          # Data models (chat history, metadata)
│   ├── services/        # Business logic (RAG pipeline, content processing)
│   ├── api/             # FastAPI endpoints
│   └── core/            # Configuration, database connections
├── requirements.txt     # Python dependencies
└── tests/               # Backend tests

frontend/
├── src/
│   ├── components/      # React components (ChatKit widget)
│   ├── pages/           # Custom pages if needed
│   └── services/        # Frontend services
└── static/              # Static assets

api/
├── main.py              # FastAPI application entry point
├── endpoints/           # API route definitions
└── utils/               # Utility functions

# Infrastructure and deployment
.infra/
├── docker-compose.yml   # Local development setup
└── deployment/          # Deployment configurations

# Existing project files
├── package.json         # Node.js dependencies
├── docusaurus.config.js # Docusaurus configuration
├── sidebars.js          # Navigation structure
└── README.md            # Project documentation
```

**Structure Decision**: Multi-component architecture with Docusaurus frontend for the book content, FastAPI backend for the RAG pipeline, and integrated chatbot widget. This approach separates concerns while maintaining tight integration between the book content and the RAG system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|.
