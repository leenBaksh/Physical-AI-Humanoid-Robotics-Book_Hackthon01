<!-- Sync Impact Report:
     Version change: N/A (initial version) → 1.0.0
     Modified principles: N/A (new constitution)
     Added sections: All sections (new constitution)
     Removed sections: N/A
     Templates requiring updates: N/A (new constitution)
     Follow-up TODOs: None
-->
# Unified AI-Generated Book with Embedded RAG Chatbot Constitution

## Core Principles

### I. Spec-Driven Development
The entire book must be written using Claude Code with Spec-Kit Plus as the primary framework. All content creation, architectural decisions, and implementation tasks must follow the Spec-Driven Development methodology with proper specifications, plans, and task breakdowns.

### II. Full Integration
The published book must contain a fully functional RAG chatbot embedded within it as a cohesive feature. The chatbot is not a separate application but an integrated component of the book itself, providing seamless user experience.

### III. Content Integrity
The chatbot must answer questions based only on the book's actual content. Answers must be strictly grounded in the provided book text with no external knowledge unless explicitly specified in the book content itself.

### IV. User-Centric Selection
The chatbot must be capable of answering questions based on user-selected text from the book. This includes general Q&A about the entire book's content as well as context-specific Q&A based on user-highlighted or selected text passages.

### V. Production-Ready Code Quality
All code (book build, RAG pipeline, API) must be production-ready, documented, and hosted per specifications. Code must follow best practices for maintainability, security, and performance.

### VI. Technology Stack Compliance
Adherence to the specified technology stack: Docusaurus for book generation, GitHub Pages for deployment, OpenAI Agents/ChatKit SDKs with FastAPI backend, Neon Serverless Postgres for chat history/metadata, and Qdrant Cloud Free Tier for book content embeddings.

## Technical Standards

### Book Stack
Docusaurus for generation and GitHub Pages for deployment. The book must be well-formatted, responsive, and accessible via public GitHub Pages hosting.

### RAG Stack
SDK/API: OpenAI Agents/ChatKit SDKs with FastAPI backend. Database: Neon Serverless Postgres for chat history/metadata. Vector Store: Qdrant Cloud Free Tier for book content embeddings.

### Chatbot Functionality Requirements
- General Q&A about the entire book's content
- Context-specific Q&A based on user-highlighted or selected text passages
- Strict content grounding with no external knowledge injection
- Reliable and accurate response generation

## Development Workflow

### Primary Tools Mandate
Claude Code and Spec-Kit Plus are mandatory for the book authoring phase. All content creation, specification, planning, and task management must utilize these tools as specified in the project requirements.

### Quality Assurance Process
- Book Published: Complete, well-formatted book must be live on GitHub Pages
- Chatbot Operational: Embedded RAG chatbot must be active and responsive on the live book site
- Accuracy Test: Chatbot must correctly answer questions using the book as its sole knowledge source
- Selection Feature: "Answer based on selected text" feature must work reliably and accurately
- Repo Integrity: GitHub repository must contain all source code, build scripts, and clear setup instructions for full reproducibility

## Governance

The constitution governs all development activities for this project. All implementation must comply with these principles. Amendments to this constitution require explicit documentation of the changes, approval from project stakeholders, and a migration plan for existing codebase if needed. All pull requests and code reviews must verify compliance with these principles. The GitHub repository must maintain all source code, build scripts, and setup instructions to ensure full reproducibility of the system.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
