# AI-Dev-Jobs-Tracker-ETL-Pipeline

 A modular, production-grade **ETL (Extract, Transform, Load)** pipeline orchestrated by **Apache Airflow** to securely aggregate, clean, and write live AI market listings into a relational warehouse.

The project features a completely decoupled architecture, keeping core data engineering operations isolated from the orchestration framework to maximize local testability and deployment flexibility.

---
## Pipeline Architecture

![AI-Dev-Jobs-Tracker-ETL-Pipeline](images/your-exported-diagram.svg)


##  Project Structure

```text
ai-jobs-etl-pipeline/
│
├── airflow/
│   └── dags/
│       └── ai_jobs_etl_dag.py # Clean Airflow DAG orchestrator
│
├── src/                       # Core ETL operational package
│   ├── __init__.py
│   ├── config.py              # Configurations & centralized logger
│   ├── extract.py             # REST API consumption module
│   ├── transform.py           # Pandas data validation & engineering
│   └── load.py                # Transaction-safe PostgreSQL ingestion
│
├── tests/                     # Unit testing layer (mirrors src/)
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── .env.example               # Template file for environment variables
├── .gitignore                 # System & environment exclusion filters
├── Dockerfile                 # Custom Airflow worker container
├── docker-compose.yml         # Local stack deployment blueprint
└── requirements.txt           # Pinned python package dependencies
```

---

##  Architecture & Core Components

* **Orchestration (`Apache Airflow`):** Manages task graph execution state, failure propagation logic, task routing, and transient network retries.
* **Extract (`Requests`):** Pulls live tracking arrays safely from the [AI Dev Jobs REST API](https://aidevboard.com).
* **Transform (`Pandas`):** Enforces data boundary typings, normalizes nested arrays to tabular structures, strips string whitespace, and computes pipeline system metrics.
* **Load (`Psycopg2`):** Handles safe bulk processing using relational `ON CONFLICT` constraints, updating existing key updates natively without runtime row collision errors.

---

##  Getting Started

### 1. Local Testing Setup
To set up, test, and run the core ETL steps locally without spinning up Docker infrastructure:

```bash
# Clone the repository
git clone https://github.com
cd ai-jobs-etl-pipeline

# Configure a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install localized application packages
pip install -r requirements.txt
```

### 2. Configure Environment Parameters
Copy the example template file to create your active configurations framework:
```bash
cp .env.example .env
```
Open `.env` and fill in your target system credentials.

### 3. Execution of Unit Tests
Run the entire comprehensive test runner suite natively:
```bash
pytest -v
```

---

##  Containerized Production Deployment

The project includes pre-configured environment orchestrations to deploy a local production sandbox containing both an Apache Airflow worker cluster and an isolated PostgreSQL datastore.

Run the stack using Docker Compose:
```bash
docker-compose up --build -d
```

* **Airflow Web UI Portal:** Available locally at `http://localhost:8080` (Default credentials: `airflow` / `airflow_secure_pass`).
* **Active Pipeline Runs:** Toggle the `ai_jobs_etl_pipeline` DAG to active inside the web interface to kick off automated daily data pulls.

---

##  Database Target Data Schema

Target tables scale dynamically using the following structured structural matrix layout:

| Field | Type | Description |
| :--- | :--- | :--- |
| `job_id` | `VARCHAR(100)` | **Primary Key** — Unique item tracking key from API |
| `title` | `VARCHAR(255)` | Cleansed role target title |
| `company` | `VARCHAR(255)` | Hiring company entity name |
| `location` | `VARCHAR(255)` | Geographic context parameters |
| `salary_min` | `INT` | Target compensation lower bound (USD) |
| `salary_max` | `INT` | Target compensation upper bound (USD) |
| `tags` | `TEXT` | Skillsets and framework categorizations |
| `extracted_at` | `TIMESTAMP` | Operational processing run timestamp |

# License

This project is open-source and licensed under the terms of the [MIT LICENSE](MIT).
