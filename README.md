# BHCPF Backend

Backend service for the BHCPF health facilities and benefits directory, built with **FastAPI** and connected to a hosted **Supabase** PostgreSQL database. This service powers the AI RAG (Retrieval-Augmented Generation) pipeline for querying healthcare benefits and facility locations in Plateau State.

## Project Architecture

- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Data**: 133 cleaned BHCPF facilities and 23 National Benefit Rules
- **AI**: Gemini 2.5 Flash for semantic search and conversational AI

## Getting Started

Because the database is centrally hosted, **you do not need to create your own Supabase project**. You just need the shared `.env` credentials to connect to the existing database.

### 1. Clone the repository
```bash
git clone https://github.com/mayowa-kalejaiye/bhcpf-backend.git
cd bhcpf-backend
```

### 2. Set up Environment Variables
Request the `.env` file from the team lead and place it in the root `bhcpf-backend` directory. It must contain:
```env
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
GEMINI_API_KEY=AIza...
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
```

### 4. Run the Development Server
Make sure you navigate into the `backend` folder before running the server:
```bash
cd backend
uvicorn app.main:app --reload
```
The API will be running at `http://localhost:8000`.
You can view the interactive Swagger API documentation at **`http://localhost:8000/docs`**.

---

## API Documentation

The backend exposes three core endpoints for the frontend to consume.

### 1. AI Chat Orchestrator
This endpoint powers the conversational RAG pipeline. It receives a user query, automatically queries the database for relevant context, and uses the AI to form an accurate response.

- **URL:** `/api/chat/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "message": "Where can I get free malaria treatment?",
    "lga": "Kanke",
    "ward": "Namu"
  }
  ```
  *(Note: `lga` and `ward` are optional string parameters to localize the search).*
- **Response:**
  ```json
  {
    "answer": "Malaria treatment is covered at the Primary level at your Registered PHC. You can visit PHC Namu in your ward.",
    "lga_searched": "Kanke",
    "ward_searched": "Namu"
  }
  ```

### 2. Facilities Directory
Fetch a list of registered PHCs, optionally filtering by Local Government Area and Ward.

- **URL:** `/api/facilities`
- **Method:** `GET`
- **Query Parameters:**
  - `lga` (optional)
  - `ward` (optional)
- **Example Usage:** `/api/facilities?lga=Bokkos`
- **Response:**
  ```json
  {
    "facilities": [
      {
        "id": 1,
        "facility_name": "PHC Bokkos",
        "lga": "Bokkos",
        "ward": "Bokkos",
        "state": "Plateau",
        "created_at": "2023-10-01T12:00:00Z"
      }
    ]
  }
  ```

### 3. Benefit Rules
Fetch official BHCPF benefit package rules.

- **URL:** `/api/benefits`
- **Method:** `GET`
- **Query Parameters:**
  - `category` (optional, e.g., "Maternal")
  - `service` (optional)
- **Example Usage:** `/api/benefits?category=Maternal`
- **Response:**
  ```json
  {
    "benefits": [
      {
        "id": 5,
        "service": "Family planning, antenatal, postnatal",
        "category": "Maternal",
        "level": "Primary",
        "details": "...",
        "limits": "...",
        "access_point": "Registered PHC"
      }
    ]
  }
  ```

---

## Testing
We use `pytest` for automated integration testing. To run the test suite:
```bash
cd backend
python -m pytest
```

## Project Structure
- `backend/app/main.py`: Main FastAPI application entry point.
- `backend/app/api/`: API route handlers.
- `backend/app/services/`: Contains `ai_service.py` handling the Gemini integration.
- `backend/tests/`: Automated pytest suite mocking the AI and querying DB.
- `backend/seed_db.py`: The script used to upload the raw data to Supabase.
