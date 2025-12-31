# Research: Physical AI & Humanoid Robotics Book with RAG Chatbot

## Decision: Multi-Component Architecture with Docusaurus and FastAPI

**Rationale**: A multi-component architecture with Docusaurus for the book frontend and FastAPI for the RAG backend provides the best separation of concerns while maintaining tight integration. Docusaurus excels at documentation sites with excellent search and navigation features, while FastAPI provides high-performance API capabilities with automatic documentation.

**Alternatives considered**:

- Single monolithic application: Would mix concerns and make deployment more complex
- Static site with client-side RAG: Would expose vector database directly to clients
- Pure server-side rendering: Would limit the rich documentation features of Docusaurus

## Decision: Qdrant Vector Database for Content Storage

**Rationale**: Qdrant is specifically designed for vector similarity search and integrates well with Python-based RAG pipelines. It supports the free tier required by the constitution and provides excellent performance for semantic search of book content.

**Alternatives considered**:

- Pinecone: More expensive, vendor lock-in concerns
- Weaviate: More complex setup, less mature Python SDK
- ChromaDB: Simpler but less scalable for production use

## Decision: Neon Serverless Postgres for Metadata Storage

**Rationale**: Neon provides serverless Postgres with excellent performance and scalability. It integrates well with Python applications and provides the metadata storage needed for the RAG system (chat history, user sessions, etc.) while supporting the free tier.

**Alternatives considered**:

- Supabase: More features but potentially more complex
- PlanetScale: MySQL-based, less familiar for Python ecosystem
- In-memory storage: Not suitable for production use

## Decision: ChatKit SDK for Frontend Integration

**Rationale**: ChatKit provides a pre-built, customizable chat interface that can be easily embedded in Docusaurus sites. It handles UI complexity while allowing customization for the book's specific needs.

**Alternatives considered**:

- Custom React chat component: More development time, reinventing the wheel
- Third-party chat widgets: Less control over integration with book content
- Vanilla JavaScript implementation: More complex and error-prone

## Decision: GitHub Pages for Book Deployment

**Rationale**: GitHub Pages provides free, reliable hosting for static sites with excellent integration with GitHub workflows. It's ideal for documentation sites and meets the requirement for public accessibility.

**Alternatives considered**:

- Netlify: More features but not required for this use case
- Vercel: Good alternative but GitHub Pages is sufficient and free
- Self-hosted: More complex with no additional benefits

## Decision: Railway for RAG API Deployment

**Rationale**: Railway provides easy deployment for FastAPI applications with support for environment variables, databases, and scaling. It offers a free tier that meets the project's requirements.

**Alternatives considered**:

- Heroku: Decreasing free tier support
- Render: Good alternative but Railway has simpler setup
- AWS/GCP: Overkill for this project's requirements
