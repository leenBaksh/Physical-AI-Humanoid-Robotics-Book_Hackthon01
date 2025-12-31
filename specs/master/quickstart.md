# Quickstart Guide: Physical AI & Humanoid Robotics Book with RAG Chatbot

## Prerequisites

Before starting with the Physical AI & Humanoid Robotics book project, ensure you have the following installed:

1. **Node.js**: Version 18+ for Docusaurus
2. **Python**: Version 3.11+ for FastAPI backend
3. **Git**: For version control
4. **Docker**: For local development (optional but recommended)

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Frontend Dependencies

```bash
# Navigate to the project root
cd D:\Physical-AI---Humanoid-Robotics

# Install Node.js dependencies
npm install
```

### 3. Set Up Backend Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory with the following:

```env
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=your_neon_db_connection_string
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

## Running the Book Locally

### 1. Start the Docusaurus Development Server

```bash
# From the project root
npm run start
```

This will start the book site on `http://localhost:3000`.

### 2. Start the RAG Backend API

```bash
# From the backend directory
cd backend
# Activate your virtual environment first
python -m uvicorn api.main:app --reload --port 8000
```

This will start the RAG API on `http://localhost:8000`.

## Adding Book Content

### 1. Module Structure

The book is organized into modules. To add a new module:

```text
docs/
├── module1/           # Module 1: ROS 2 Fundamentals
│   ├── index.md
│   ├── chapter-1-ros2-core/
│   │   ├── index.md
│   │   └── content.md
│   └── chapter-2-ai-ros-bridge/
│       ├── index.md
│       └── content.md
├── module2/           # Module 2: Digital Twin (Gazebo & Unity)
│   ├── index.md
│   └── chapter-1-gazebo-fundamentals/
│       ├── index.md
│       └── content.md
```

### 2. Adding New Content

1. Create new `.md` files in the appropriate module directory
2. Update `sidebars.js` to include the new content in navigation
3. Add any code snippets or configuration examples in the appropriate format

## Running the RAG Pipeline

### 1. Index Book Content

```bash
# From the backend directory
cd backend
python -m src.services.content_processor --index-all
```

This will process all book content and store embeddings in Qdrant.

### 2. Test the API

```bash
# Query the RAG system
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the core concepts of ROS 2?",
    "session_id": "test-session"
  }'
```

## Deploying the Book

### 1. Building for Production

```bash
# Build the Docusaurus site
npm run build
```

### 2. Deployment to GitHub Pages

```bash
# Deploy to GitHub Pages
npm run deploy
```

### 3. Deploying the RAG API

1. Push the backend code to a deployment platform like Railway
2. Configure the environment variables in the deployment platform
3. Ensure the deployment platform can connect to Neon DB and Qdrant

## Working with the Chatbot

### 1. Integration with Docusaurus

The chatbot is integrated via the ChatKit widget. To customize:

1. Modify components in the `frontend/src/components/` directory
2. Update the API endpoint configuration in the chatbot initialization
3. Test the integration by running both frontend and backend locally

### 2. Text Selection Feature

The chatbot supports context-specific Q&A based on selected text:

1. Users can highlight text in the book content
2. The chatbot will provide answers specifically related to the selected text
3. This is implemented through the message context in the API

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port numbers in the start commands
2. **API connection errors**: Verify that the backend is running and environment variables are correct
3. **Content not showing**: Check that the file is in the correct location and referenced in sidebars.js
4. **RAG queries returning no results**: Verify that the content has been indexed in Qdrant

### Checking System Status

```bash
# Check if the RAG API is running
curl http://localhost:8000/health

# Check if the Docusaurus site is running
curl http://localhost:3000
```

## Next Steps

1. Complete Module 1 content (ROS 2 fundamentals)
2. Implement Module 2 content (Gazebo/Unity digital twin)
3. Integrate the RAG pipeline with the book content
4. Deploy the complete system to production
