 # TaxAI Agent 

An AI-powered tax document processing system built with **Python, FastAPI, React, LangGraph, RAG, OCR, and LLMs**.

TaxAI Agent is designed to automate the initial processing of tax-related documents, extract structured information, validate the extracted data, apply tax rules, and route cases for human/CA review.


---

## 🚀 Project Workflow

```text
Document Upload
       ↓
FastAPI
       ↓
Document Storage
       ↓
OCR (Tesseract)
       ↓
OCR Text
       ↓
LLM Extraction
       ↓
Structured Data
       ↓
Validation
       ↓
Missing Information
       ↓
Tax Rules RAG
       ↓
Tax Calculation
       ↓
Final Validation
       ↓
CA Review
       ↓
Case Summary
```

---

## 📄 Supported Documents

The application is designed to process:

* PAN Card
* Aadhaar Card
* Salary Slips
* Bank Statements
* Form 16

Supported formats:

```text
JPG
JPEG
PNG
PDF
```

> PDF OCR processing is currently under development.

---

## 🧠 AI Workflow

The backend uses **LangGraph** to orchestrate the tax-processing workflow.

Current workflow includes:

```text
Classify Documents
        ↓
Extract Salary Data
        ↓
Check Missing Information
        ↓
Validate Salary Data
        ↓
Calculate Annual Income
        ↓
Tax Rules RAG
        ↓
Calculate Tax
        ↓
Final Validation
        ↓
CA Review
        ↓
Generate Case Summary
```

The workflow also supports a human-in-the-loop path when required information is missing.

---

## 🔎 OCR Pipeline

Image documents are processed using **Tesseract OCR**.

```text
JPG / PNG
    ↓
Pillow
    ↓
Tesseract
    ↓
Extracted Text
```

The extracted text is then passed to an LLM for structured information extraction.

Example:

```text
Basic Salary: 60000
HRA: 20000
Other Allowance: 10000
Gross Salary: 90000
TDS: 5000
Net Salary: 85000
```

can be converted into:

```json
{
  "basic_salary": 60000,
  "hra": 20000,
  "other_allowance": 10000,
  "gross_salary": 90000,
  "tds": 5000,
  "net_salary": 85000
}
```

---

## 🧩 Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Python Multipart

### AI / Agent

* LangGraph
* OpenRouter
* LLM-based structured extraction

### RAG

* ChromaDB
* Sentence Transformers
* Tax-rule retrieval

### Document Processing

* Tesseract OCR
* PyTesseract
* Pillow
* PDF processing *(in development)*

---

## 📁 Project Structure

```text
TaxAI-Agent/
│
├── backend/
│   ├── main.py
│   ├── document_reader.py
│   ├── llm_extractor.py
│   ├── rag/
│   │   └── ...
│   ├── uploads/
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .gitignore
├── README.md
└── ...
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/priyadixit123/TaxAI-Agent.git
cd TaxAI-Agent
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install backend dependencies:

```powershell
pip install fastapi uvicorn python-multipart pillow pytesseract pdf2image
```

Install frontend dependencies:

```powershell
cd frontend
npm install
```

---

## 🔐 Environment Variables

Create:

```text
backend/.env
```

Add your API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Never commit `.env` files or API keys to GitHub.

---

## ▶️ Running the Backend

From the project root:

```powershell
venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Running the Frontend

Open another terminal:

```powershell
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🔒 Security

This project is currently intended for development and portfolio demonstration.

Do **not** upload real:

* PAN cards
* Aadhaar cards
* Bank statements
* Salary documents
* Other sensitive personal information

Use dummy or masked documents during development.

A production implementation would require:

* Authentication and authorization
* Encryption
* Secure document storage
* Access control
* Audit logging
* Data retention policies
* Secure identity verification
* Production-grade database
* Privacy controls

---

## 📌 Current Features

* ✅ React-based TaxAI interface
* ✅ Login / Signup UI
* ✅ Multi-document upload
* ✅ FastAPI upload API
* ✅ Local document storage
* ✅ Tesseract OCR integration
* ✅ LLM-based structured extraction
* ✅ LangGraph workflow
* ✅ Salary data validation
* ✅ Missing-information workflow
* ✅ Human-in-the-loop flow
* ✅ Tax rules RAG prototype
* ✅ Tax calculation prototype
* ✅ CA review workflow

---

## 🔮 Future Improvements

* [ ] Complete PDF OCR pipeline
* [ ] Vision-based document extraction
* [ ] Better document classification
* [ ] Structured output validation with Pydantic
* [ ] PostgreSQL database
* [ ] Secure authentication
* [ ] CA dashboard
* [ ] Client case management
* [ ] RAG evaluation
* [ ] Advanced tax calculations
* [ ] Official tax-rule integration
* [ ] GST module
* [ ] Production deployment
* [ ] Monitoring and observability

---

## 🎯 Learning Goals

This project is being developed to explore real-world **Agentic AI and AI Automation engineering**, including:

* LangGraph orchestration
* Tool-based AI workflows
* RAG
* OCR
* LLM structured extraction
* Human-in-the-loop systems
* FastAPI
* React
* Document processing
* AI validation pipelines

---

## 👩‍💻 Author

**Priya Dixit**

GitHub: [@priyadixit123](https://github.com/priyadixit123)

---

## ⭐ Project Status

🚧 **Actively under development**

The project is being built incrementally from document upload → OCR → structured extraction → LangGraph → RAG → validation → CA review.
