# MCP Email Fetch

## Overview
**MCP Email Fetch** is an AI-powered email assistant that integrates the **Model Context Protocol (MCP)** to fetch, process, rank, and summarize emails. It leverages LLM-based sentiment analysis and a vector store for efficient retrieval. The project consists of a **Python-based backend** and an **MCP server** for seamless interaction.

## Features
- **Email Fetching**: Retrieves emails from Gmail.
- **AI-Powered Summarization**: Extracts key insights from emails.
- **Sentiment Analysis**: Determines email sentiment for prioritization.
- **Email Ranking**: Uses an LLM-based ranking system.
- **FAISS Vector Store**: Stores email embeddings for efficient retrieval.
- **Automatic Replies**: Generates AI-powered responses to emails.
- **Dashboard API**: Provides endpoints for user interaction.

## Project Structure
```
└── hiteshydv001-mcp-email-fetch/
    ├── backend/
    │   ├── main.py                  # Main entry point for backend API
    │   ├── requirements.txt         # Dependencies for backend
    │   ├── ai/
    │   │   ├── email_ranker.py       # AI-powered email ranking
    │   │   ├── llm_handler.py        # Handles interactions with LLM
    │   │   └── sentiment_analysis.py # Sentiment classification
    │   ├── config/
    │   │   ├── config.py             # General configuration
    │   │   ├── logging_config.py     # Logging configuration
    │   │   ├── mcp_config.py         # MCP-specific settings
    │   │   ├── token.json            # Google API authentication token
    │   │   └── secrets.json          # Google API client secrets
    │   ├── database/
    │   │   ├── db.py                 # Database connection
    │   │   └── models.py             # Database models
    │   ├── email_processing/
    │   │   ├── email_reply.py        # AI-generated replies
    │   │   ├── email_summarizer.py   # Summarizes email content
    │   │   └── gmail_fetch.py        # Fetches emails from Gmail
    │   ├── mcp/
    │   │   ├── faiss_vectorstore.py  # FAISS-based email storage
    │   │   └── mcp_retriever.py      # Retrieves relevant emails
    │   ├── routes/
    │   │   ├── dashboard_routes.py   # API routes for dashboard
    │   │   └── email_routes.py       # API routes for emails
    │   └── utils/
    │       ├── logger.py             # Logging utilities
    │       ├── preprocess.py         # Data preprocessing
    │       └── token_manager.py      # Token authentication
    └── mcp-server/
        ├── package-lock.json
        ├── package.json
        ├── tsconfig.json             # TypeScript config for MCP server
        ├── dist/
        │   └── index.js              # Compiled MCP server
        └── src/
            └── index.ts              # MCP server implementation
```

## Installation
### Backend Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/Hiteshydv001/mcp-email-fetch.git
   cd mcp-email-fetch/backend
   ```
2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables and Google API authentication**:
   - Obtain **Google Cloud Email API credentials**.
   - Download `token.json` and `secrets.json` from Google Cloud Console.
   - Place them inside the `config/` directory.
   - Ensure `gmail_fetch.py` uses these credentials.
   - Create a `.env` file in the `backend/` directory and add:
     ```ini
     MONGODB_URI=your_mongodb_connection_string
     GEMINI_API_KEY=your_gemini_api_key
     GMAIL_SECRET_KEY=your_gmail_secret_key
     DEBUG=True
     ```

5. **Run the backend server**:
   ```sh
   python main.py
   ```

### MCP Server Setup
1. **Navigate to the `mcp-server` directory**:
   ```sh
   cd ../mcp-server
   ```
2. **Install dependencies**:
   ```sh
   npm install
   ```
3. **Run the MCP server**:
   ```sh
   npm run start
   ```

## Usage
- Use the **API endpoints** to fetch, summarize, and reply to emails.
- Interact via a **dashboard** to view email sentiment and ranking.
- Automate email responses with **LLM-generated replies**.

## Contributing
Feel free to contribute by submitting issues or pull requests.

## License
This project is licensed under the MIT License.

---
🚀 **Developed by Hitesh Kumar**

