# F1 Information Chatbot

An interactive chatbot system that provides detailed Formula 1 information, including driver statistics, race results, team performance, championship history, and more. The project features a Python backend and a modern React frontend.

---

## Features

- Query driver statistics, race results, team performance, and championship history
- Compare drivers, teams, and multi-year trends
- Natural language understanding for conversational queries
- Well-formatted responses (tables, explanations)
- Context-aware follow-up questions

---

## Folder Structure
```
F1 Chatbot/
│
├── backend/           # Python backend (API, database, logic)
│   ├── init .py
│   ├── main.py
│   ├── database.py
│   ├── llm_query.py
│   └── .env           # (not included in repo)
│
├── data/
│   └── f1_database.db # (optional, not included in repo)
│
├── frontend/          # React + Vite + TailwindCSS web app
│   └── ...            # (see frontend/README.md for details)
│
├── prd.md             # Product requirements document
├── schema.md          # Database schema
├── README.md          # This file
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm (for frontend)
- (Recommended) [Poetry](https://python-poetry.org/) or `venv` for Python dependencies

### Backend Setup

1. **Install dependencies**  
   ```bash
   cd backend
   pip install -r requirements.txt

2. **Configure environment variables**
   Create a .env file in backend/ (see .env.example if available).

3. **Run the backend server**
   ```bash
   uvicorn backend.main:app --reload

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install

2. **Run the frontend server**
   ```bash
   npm run dev

### Usage

- Access the web app at http://localhost:5173 (or the port shown in your terminal)
- Ask questions about Formula 1 (historical fact, statistics, general information, etc)
- Not suited for live sessions of future information


### Acknowledgments

- Formula 1 Datbase made with the F1 dataset in Kaggle https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020 (full with all data from 1950 til 2024 even though the link only says 2020)  by VOPANI.

- Used GROQ API and implemented the LLAMA3 models (8b and 70b)

- Used React, Vite, TailwindCSS, and Vercel for the frontend

- Used Python, FastAPI, and SQLite for the backend


