# Smart Recruitment System

This graduation project helps job seekers find positions that match their resumes. It provides a **Streamlit** user interface and a **Django REST Framework** backend, and uses **CrewAI** agents to analyze resumes and compare candidates' skills with job listings.

## How It Works

1. The user signs in or creates an account through the interface.
2. The user uploads a resume in PDF format and enters the desired job title, location, job description, and expected salary.
3. The system extracts technical skills from the resume and searches for job listings using Serper.
4. An AI agent evaluates the listings and returns results with match scores and links to the original postings.
5. Searches and results are saved so users can view their previous search history when they sign in again.

> Resume processing extracts text from PDF files. Scanned PDFs that contain images instead of extractable text may not be readable.

## Requirements

- Python 3.10 or newer.
- An internet connection to access an AI provider and Serper.
- An API key for an LLM provider: **Groq** or **OpenAI**.
- A **Serper** API key for job searches.

## Setup and Run on Windows

Run the following commands from the project directory in PowerShell.

### 1. Create a Python Environment and Install Dependencies

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell prevents environment activation, run commands using the Python executable inside the virtual environment, for example:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Configure API Keys

Create a file named `.env` in the project root and add your API keys. Provide at least one LLM provider key, along with a Serper key:

```dotenv
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

Alternatively, use OpenAI instead of Groq:

```dotenv
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

The project uses Groq when `GROQ_API_KEY` is set; otherwise, it uses OpenAI. Do not commit the `.env` file or share your API keys. The file is excluded from Git through `.gitignore`.

### 3. Prepare the Database and Run the Backend

In the first PowerShell window:

```powershell
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

The backend provides the user sign-in endpoint at `http://127.0.0.1:8000/user/` and the resume and job-details submission endpoint at `http://127.0.0.1:8000/details/`. Data is stored locally in the SQLite database file `db.sqlite3`.

### 4. Run the Streamlit Interface

Open a second PowerShell window in the project directory, activate the virtual environment, and run:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app\app.py
```

Open the URL shown in the terminal, usually `http://localhost:8501`. Keep both the backend and interface windows open while using the application.

## Notes

- The local interface connects to the backend at `http://127.0.0.1:8000`, so Django must be running before submitting requests through Streamlit.
- The root `requirements.txt` file contains the backend and interface dependencies.
- The default settings are intended for local development, not production deployment.
