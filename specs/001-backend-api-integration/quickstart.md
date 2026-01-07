# Quickstart: Backend API & Frontend Integration

## Overview
This guide explains how to set up and run the FastAPI backend with the Docusaurus frontend chat interface for local development.

## Prerequisites
- Python 3.11+
- Node.js and npm for Docusaurus
- Access to OpenAI API with valid API key
- Properly configured `.env` file with API keys:
  - `OPENAI_API_KEY` for OpenAI access
  - `OPENROUTER_API_KEY` for OpenRouter access (optional)

## Setup

### 1. Backend Setup
1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn python-dotenv openai-agents
   ```

2. Ensure your environment is properly configured:
   ```bash
   # Make sure you have the required environment variables in .env:
   OPENAI_API_KEY=your_openai_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key (optional)
   ```

### 2. Frontend Setup
1. Navigate to the Docusaurus directory:
   ```bash
   cd frontend_robotic_book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### 1. Starting the Backend
To start the FastAPI backend:

```bash
uvicorn api:app --reload --port 8000
```

This will:
- Start the API server on `http://localhost:8000`
- Make the `/chat` endpoint available
- Enable session management for conversations

### 2. Starting the Frontend
To start the Docusaurus frontend:

```bash
cd frontend_robotic_book
npm run start
```

This will:
- Start the Docusaurus development server on `http://localhost:3000`
- Load the chat interface component
- Connect to the backend API

## Using the Chat Interface

Once both servers are running:

1. Visit the Docusaurus site at `http://localhost:3000`
2. Locate the chat interface component
3. Enter your questions about the book content
4. The system will:
   - Send your message to the backend API
   - Process it through the BookAgent
   - Return responses with source citations
   - Maintain conversation history in the session

## API Endpoint

### POST /chat
- **Description**: Process a user message and return an AI response
- **Request Body**:
  ```json
  {
    "message": "Your question here",
    "session_id": "unique-session-identifier"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "The AI's response",
    "citations": [
      {
        "url": "source-url",
        "title": "Source Title"
      }
    ],
    "session_id": "unique-session-identifier",
    "timestamp": "2026-01-02T05:00:00Z"
  }
  ```

## Expected Behavior

### Successful Response
- Frontend sends user message to backend API
- Backend processes message through BookAgent
- Response includes answer and source citations
- Conversation history is maintained per session

### Error Handling
- If backend is unavailable, frontend shows appropriate error message
- If BookAgent fails, system returns graceful error response
- Invalid requests receive appropriate HTTP status codes

## Troubleshooting

- If you get API errors, verify your OpenAI API keys are correct
- If frontend can't connect to backend, check CORS configuration
- If responses seem irrelevant, ensure the BookAgent is properly configured
- For timeout errors, check your network connection to external services