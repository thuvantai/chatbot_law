# Legal Document Chatbot

This is a Retrieval-Augmented Generation (RAG) chatbot that allows you to upload legal documents (PDF, DOCX) or provide Web URLs, and then interactively ask questions about their contents.

## Features
- **Document Support**: Parses PDF and DOCX files.
- **Web Support**: Scrapes and parses text from Web URLs.
- **RAG Architecture**: Uses ChromaDB for vector storage and retrieval.
- **Gemini LLM**: Powered by Google's Gemini 1.5 Pro and Gemini embedding models for high accuracy and context understanding.

## Requirements
You need to have Python installed. The required packages are listed in `requirements.txt`.

## How to Run (Using Docker - Recommended)
The easiest way to run the application and avoid local environment issues is using Docker.

1. Ensure you have **Docker Desktop** installed and running.
2. Create your `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   *And open `.env` to add your Google API Key if you want it pre-configured.*
3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Open the provided Local URL (e.g., http://localhost:8501) in your browser.

## How to Run (Locally)
1. If you haven't already, install the dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the Streamlit application:
   ```bash
   python -m streamlit run app.py
   ```
3. Open the provided Local URL (e.g., http://localhost:8501) in your browser.

## Note
- Ensure you upload valid `.pdf` or `.docx` files.
- Older `.doc` files may not be supported by the DOCX parser; please save them as `.docx` first.
