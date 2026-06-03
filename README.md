# C-DIVE-Construction-Data-Integration-Verification-Engine-
C-DIVE is a full-stack, AI-powered pipeline designed to automate the extraction and mathematical verification of high-volume multifamily construction invoices.
Built to solve the problem of manual CapEx budget variance tracking, this application leverages Google's Gemini 2.5 Flash model for intelligent text extraction, wrapped in a strict deterministic Python layer that mathematically proves the LLM's output before it ever reaches a human reviewer.

🏗️ Architecture & Engineering Choices
Because large language models can hallucinate or fail at arithmetic, this system is designed around a "Trust, but Verify" architecture:

In-Memory File Processing: To maintain strict data security, uploaded PDF invoices are parsed into byte streams (io.BytesIO) and read directly in memory using PyPDF2. Files are never saved to a local hard drive.

Type-Safe Extraction: The instructor library forces the Gemini model to respond in a strictly validated JSON schema defined by Python Pydantic models, preventing malformed data from crashing the frontend.

Deterministic Fail-Safes: Before returning data, the FastAPI backend iterates through the AI-extracted line items, recalculates the sum, and checks for variance against the extracted total. Invoices with a variance > $0.00 are instantly flagged with a "Red" status and a specific error message.

Decoupled System: A Next.js frontend communicates with the FastAPI backend via a configured CORS bridge, allowing the core extraction engine to be easily integrated into mobile apps (like React Native) or internal enterprise dashboards in the future.

🛠️ Tech Stack
Frontend: Next.js, React, Tailwind CSS, TypeScript

Backend: Python, FastAPI, Uvicorn

AI & Parsing: Google Gemini 2.5 Flash, instructor, Pydantic, PyPDF2

Testing: pytest, httpx

🚀 Getting Started (Local Development)
Prerequisites
Python 3.10+

Node.js v18+

A valid Google Gemini API Key

1. Backend Setup
Navigate to the backend directory, create a virtual environment, and install dependencies:

Bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Mac/Linux use: source venv/bin/activate
pip install -r requirements.txt
Set your API key as an environment variable, then start the FastAPI server:

Bash
uvicorn main:app --reload
The backend will be running at http://localhost:8000 with interactive API documentation available at http://localhost:8000/docs.

2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the Next.js development server:

Bash
cd frontend
npm install
npm run dev
The frontend dashboard will be available at http://localhost:3000.

🧪 Automated Testing
To guarantee the integrity of the math-verification fail-safe, this project includes an automated test suite built with pytest and FastAPI's TestClient.

To run the test suite, ensure your virtual environment is active and run:

Bash
cd backend
pytest
Test Coverage Includes:

test_successful_extraction: Verifies that a mathematically sound invoice parses correctly and returns a "Green" status.

test_math_fail_safe: Injects an invoice with an intentional math error to verify that the deterministic Python layer successfully catches the LLM hallucination and flags it as "Red".
Disclaimer!
You need to add a next.js for the frontend. Code needed has been attached.
