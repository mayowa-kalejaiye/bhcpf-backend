# BHCPF Backend

Backend service for the BHCPF health facilities and benefits directory, built with **FastAPI** and connected to a hosted **Supabase** PostgreSQL database. This service powers the AI RAG (Retrieval-Augmented Generation) pipeline for querying healthcare benefits and facility locations in Plateau State.

## Project Architecture

- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL with `pgvector` for embeddings)
- **Data**: 133 cleaned BHCPF facilities and 23 National Benefit Rules
- **AI**: (Upcoming) LLM integration for semantic search and intent classification

## Getting Started

Because the database is centrally hosted, **you do not need to create your own Supabase project**. You just need the shared `.env` credentials to connect to the existing database.

### 1. Clone the repository
```bash
git clone https://github.com/mayowa-kalejaiye/bhcpf-backend.git
cd bhcpf-backend
```

### 2. Set up Environment Variables
Request the `.env` file from the team lead and place it in the root `bhcpf-backend` directory. It must contain the shared database credentials:
```env
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
# source venv/bin/activate

# Install requirements
pip install -r backend/requirements.txt
pip install python-dotenv
```

### 4. Run the Development Server
Make sure you navigate into the `backend` folder before running the server:
```bash
cd backend
uvicorn app.main:app --reload
```
The API will be running at `http://localhost:8000`.
You can view the interactive Swagger API documentation at **`http://localhost:8000/docs`**.

## Project Structure
- `backend/app/main.py`: Main FastAPI application entry point tying the routers together.
- `backend/app/api/`: API route handlers (endpoints for `/chat`, `/facilities`, `/benefits`, `/feedback`).
- `backend/seed_db.py`: The script used to clean the messy Excel sheets and upload the data to Supabase. *(Note: The database is already seeded, so you don't need to run this unless the raw data changes!)*
- `backend/data/`: Contains the raw `bhcpf_benefits.json` rules.
