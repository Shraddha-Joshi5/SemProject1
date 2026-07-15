# 🧬 High-Performance Facial Recognition Vector Engine

A fully containerized **FastAPI** web service paired with a **PostgreSQL** database layer designed to handle biometric face extraction, high-dimensional vector embedding storage, and real-time identity verification.

---s

## 🚀 System Architecture & Pipeline

The system is split into two core operations hosted inside an isolated Docker network bridge:
1. **Biometric Registration (`/register`)**: Accepts a unique name identifier paired with a strict **512-dimensional floating-point face vector matrix**. The payload is validated via Pydantic and committed via `psycopg2` transactional scripts directly to the database.
2. **Identity Verification (`/identify`)**: Receives an unknown incoming 512-dimensional face vector, queries historical records from the relational layer, executes vector distance comparison math, and returns the closest matched identity alongside a confidence score.

---

## 📂 Repository Layout

```text
├── .gitignore               # Excludes python caches and local environment blocks
├── README.md                # Project architecture and execution manual
├── Dockerfile               # Debian-slim environment + C-compilers + Python packages
├── docker-compose.yml       # Orchestrates network bindings between Web App and PostgreSQL
├── app.py                   # FastAPI routing gateway & Pydantic data validation schemas
├── database.py              # Database core configurations and initialization anchors
├── database_module.py       # SQL query execution layer and psycopg2 transaction logic
├── store_face.py            # Extracts face metrics and coordinates the registration flow
├── recognize_face.py        # Runs face recognition vector comparison math routines
└── test_module.py           # Automated diagnostic and regression test scripts
Infrastructure Lifecycle Operations
Local Compilation & Startup
To build system layers, download necessary C++ compilers, configure database hooks, and launch the server pipeline natively:

PowerShell
docker compose up --build
Direct API Testing
Once the container initializes completely and prints Application startup complete, open your local gateway:

Interactive Swagger UI Endpoint: http://localhost:8000/docs

📈 Current Milestone Status
API Validation Layers: 🟢 Complete (200 OK validated on 512-dimension vectors)

Database Query Transactions: 🟢 Complete (psycopg2 pipeline operational)

Environment Containerization: 🟢 Complete (Docker blueprint cached and live)


---

## Step 2: Create a `.gitignore` File (Crucial for a Clean Repo)

We do not want to accidentally upload messy temporary Python files or system caches to GitHub. 

1. Create a new file in your project folder named **`.gitignore`** (make sure it starts with a dot).
2. Paste these lines inside and save it:
```text
__pycache__/
*.pyc
.env
.DS_Store